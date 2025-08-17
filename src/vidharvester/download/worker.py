from __future__ import annotations

import os
import re
import traceback
from dataclasses import dataclass
import shutil
import asyncio
from typing import Optional, List

from PyQt6 import QtCore

import yt_dlp
import requests
from bs4 import BeautifulSoup
from vidharvester.capture.playwright_capture import capture_page_media


@dataclass
class DownloadOptions:
	output_directory: str
	mode: str  # "video" or "audio"
	format_str: str  # e.g., mp4 / webm / mp3
	quality: str  # yt-dlp format expression
	filename_template: str
	embed_subtitles: bool = False
	embed_thumbnail: bool = False
	user_agent: str = (
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
		"AppleWebKit/537.36 (KHTML, like Gecko) "
		"Chrome/126.0.0.0 Safari/537.36"
	)
	cookies_file: Optional[str] = None


class DownloadWorker(QtCore.QThread):
	progress_signal = QtCore.pyqtSignal(dict)
	log_signal = QtCore.pyqtSignal(str)
	finished_signal = QtCore.pyqtSignal(bool, str)

	def __init__(self, url: str, options: DownloadOptions, parent=None):
		super().__init__(parent)
		self.url = url
		self.options = options
		self._stop_flag = False
		self.last_filename: Optional[str] = None
		self.last_title: Optional[str] = None
		self.last_format: Optional[str] = None
		self.last_size: Optional[int] = None

	def stop(self):
		self._stop_flag = True

	def _hook(self, d):
		if self._stop_flag:
			raise KeyboardInterrupt("Download canceled by user")
		status = d.get("status")
		if status == "downloading":
			total = d.get("total_bytes") or d.get("total_bytes_estimate")
			downloaded = d.get("downloaded_bytes")
			speed = d.get("speed")
			eta = d.get("eta")
			filename = d.get("filename") or d.get("info_dict", {}).get("title")
			self.progress_signal.emit(
				{
					"status": "downloading",
					"filename": filename,
					"downloaded": downloaded,
					"total": total,
					"speed": speed,
					"eta": eta,
					"percent": (downloaded / total * 100.0) if downloaded and total else None,
				}
			)
		elif status == "finished":
			self.last_filename = d.get("filename") or self.last_filename
			info = d.get("info_dict") or {}
			self.last_title = info.get("title") or self.last_title
			self.last_format = info.get("ext") or self.options.format_str or self.last_format
			size = info.get("filesize") or info.get("filesize_approx")
			self.last_size = int(size) if isinstance(size, (int, float)) else self.last_size
			self.progress_signal.emit({"status": "finished", "filename": self.last_filename})

	def run(self):
		try:
			opts = self.options
			headers = {"User-Agent": opts.user_agent}

			ydl_opts = {
				"outtmpl": os.path.join(opts.output_directory, opts.filename_template),
				"restrictfilenames": False,
				"noplaylist": True,
				"nocheckcertificate": True,
				"http_headers": headers,
				"quiet": True,
				"no_warnings": True,
				"progress_hooks": [self._hook],
				"retries": 5,
				"concurrent_fragment_downloads": 5,
				"postprocessors": [],
				"writesubtitles": False,
				"writeautomaticsub": False,
				"continuedl": True,
			}

			if opts.cookies_file:
				ydl_opts["cookiefile"] = opts.cookies_file

			# Pre-extract minimal info to capture title/size when possible
			try:
				with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True, "skip_download": True}) as ydl:
					info = ydl.extract_info(self.url, download=False)
					self.last_title = info.get("title") or self.last_title
					self.last_format = info.get("ext") or self.last_format
					fs = info.get("filesize") or info.get("filesize_approx")
					self.last_size = int(fs) if isinstance(fs, (int, float)) else self.last_size
			except Exception:
				pass

			if opts.embed_subtitles:
				ydl_opts.update(
					{
						"writesubtitles": True,
						"writeautomaticsub": True,
						"subtitleslangs": ["en", ""],
					}
				)

			if opts.mode == "video":
				ydl_opts["merge_output_format"] = opts.format_str
			else:
				ydl_opts["postprocessors"].append(
					{
						"key": "FFmpegExtractAudio",
						"preferredcodec": opts.format_str,
						"preferredquality": "0",
					}
				)
				if opts.embed_thumbnail:
					ydl_opts["postprocessors"].append({"key": "FFmpegMetadata"})
					ydl_opts["writethumbnail"] = True
					ydl_opts["postprocessors"].append({"key": "EmbedThumbnail"})

			# Select format (prefer widely compatible codecs per container)
			if opts.mode == "video":
				if opts.quality and opts.quality != "auto-best":
					# Respect explicit user-provided yt-dlp format expression (e.g. 137+140)
					ydl_opts["format"] = opts.quality
				else:
					container = (opts.format_str or "").lower()
					if container == "mp4":
						# Prefer H.264 + AAC for maximum Windows compatibility
						ydl_opts["format"] = (
							"bestvideo[ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/"
							"best[ext=mp4]/best"
						)
						ydl_opts["merge_output_format"] = "mp4"
					elif container == "webm":
						ydl_opts["format"] = "bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]/best"
						ydl_opts["merge_output_format"] = "webm"
					else:  # mkv or other
						ydl_opts["format"] = "bestvideo*+bestaudio/best"
						ydl_opts["merge_output_format"] = container or "mkv"
			else:
				ydl_opts["format"] = "bestaudio/best"

			# Graceful fallback if FFmpeg is not available
			has_ffmpeg = shutil.which("ffmpeg") and shutil.which("ffprobe")
			if not has_ffmpeg:
				if opts.mode == "video":
					fmt_expr = ydl_opts.get("format", "") or ""
					# If format requires merging, fall back to progressive best
					if "+" in fmt_expr or "bestvideo" in fmt_expr:
						ydl_opts["format"] = "best[ext=mp4]/best"
						ydl_opts.pop("merge_output_format", None)
						# Remove any postprocessors that need FFmpeg
						ydl_opts["postprocessors"] = []
						self.log_signal.emit("[warn] FFmpeg not found: using progressive best without merge (set up FFmpeg for higher quality).")
				elif opts.mode == "audio":
					# Download the best audio without conversion
					ydl_opts["postprocessors"] = []
					ydl_opts["format"] = "bestaudio/best"
					self.log_signal.emit("[warn] FFmpeg not found: downloading original audio stream without conversion.")

			self.log_signal.emit("[info] Probing with yt-dlp extractor…")
			if self._download_with_ytdlp(self.url, ydl_opts):
				self.finished_signal.emit(True, "Download completed.")
				return

			self.log_signal.emit("[warn] Direct extraction failed. Trying fallback parser…")
			candidates = self._detect_media_links(self.url, opts.user_agent)
			if not candidates:
				# Try headless browser capture as a stronger fallback
				self.log_signal.emit("[warn] Fallback parser found nothing. Trying headless capture…")
				try:
					loop = QtCore.QEventLoop()
					cands: list[str] = []
					def run_async():
						async def runner():
							return await capture_page_media(self.url)
						return asyncio.run(runner())
					from concurrent.futures import ThreadPoolExecutor
					with ThreadPoolExecutor(max_workers=1) as pool:
						future = pool.submit(run_async)
						cands = future.result(timeout=45)
					candidates = cands
				except Exception as e:
					self.log_signal.emit(f"[headless-error] {e}")
					candidates = []
				if not candidates:
					raise RuntimeError("No direct media links found on the page.")
			self.log_signal.emit(f"[info] Found {len(candidates)} candidate media links.")
			for media_url in candidates:
				if self._stop_flag:
					raise KeyboardInterrupt("Canceled")
				self.log_signal.emit(f"[info] Trying media URL: {media_url}")
				if self._download_with_ytdlp(media_url, ydl_opts):
					self.finished_signal.emit(True, "Download completed (via fallback).")
					return

			raise RuntimeError("All fallback attempts failed.")

		except KeyboardInterrupt:
			self.finished_signal.emit(False, "Canceled by user.")
		except Exception as exc:
			self.log_signal.emit(traceback.format_exc())
			self.finished_signal.emit(False, f"Error: {exc}")

	def _download_with_ytdlp(self, url: str, ydl_opts) -> bool:
		try:
			with yt_dlp.YoutubeDL(ydl_opts) as ydl:
				ydl.download([url])
			return True
		except yt_dlp.utils.DownloadError as e:
			self.log_signal.emit(f"[yt-dlp] {e}")
			return False
		except Exception as e:
			self.log_signal.emit(f"[yt-dlp] Unexpected: {e}")
			return False

	def _detect_media_links(self, page_url: str, ua: str) -> List[str]:
		try:
			resp = requests.get(page_url, headers={"User-Agent": ua}, timeout=20)
			resp.raise_for_status()
		except Exception as e:
			self.log_signal.emit(f"[fallback] Failed to fetch page: {e}")
			return []

		soup = BeautifulSoup(resp.text, "html.parser")
		candidates = set()

		for tag in soup.find_all(["video", "source"]):
			src = tag.get("src")
			if src:
				candidates.add(requests.compat.urljoin(page_url, src))

		patterns = [
			r"https?://[^\s'\"<>]+\.m3u8",
			r"https?://[^\s'\"<>]+\.mpd",
			r"https?://[^\s'\"<>]+\.mp4",
			r"https?://[^\s'\"<>]+\.webm",
		]
		for pat in patterns:
			for m in re.finditer(pat, resp.text):
				candidates.add(m.group(0))

		cleaned = [u for u in candidates if not any(x in u.lower() for x in ["adserver", "doubleclick"])]
		return cleaned
