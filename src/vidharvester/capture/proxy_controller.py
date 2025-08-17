from __future__ import annotations

import os
import shutil
import subprocess
import sys
from typing import Optional

from vidharvester.utils.paths import resource_path


class ProxyController:
	"""Controls mitmproxy (mitmdump) as a subprocess with our addon.

	Note: Requires mitmproxy installed on the system (mitmdump on PATH).
	For bundled EXE users, proxy mode is optional and may require a separate installer.
	"""

	def __init__(self, port: int = 8080) -> None:
		self.port = int(port)
		self._proc: Optional[subprocess.Popen] = None

	def is_running(self) -> bool:
		return self._proc is not None and self._proc.poll() is None

	def start(self) -> None:
		if self.is_running():
			return
		mitmdump = shutil.which("mitmdump")
		if not mitmdump:
			raise RuntimeError("mitmdump not found in PATH. Install mitmproxy.")
		addon_path = resource_path(os.path.join("proxy", "mitm_addon.py"))
		args = [
			mitmdump,
			"-s",
			addon_path,
			"--listen-port",
			str(self.port),
		]
		# Start without console window on Windows
		creationflags = 0
		startupinfo = None
		if os.name == "nt":
			creationflags = subprocess.CREATE_NO_WINDOW  # type: ignore[attr-defined]
			startupinfo = subprocess.STARTUPINFO()  # type: ignore[attr-defined]
			startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW  # type: ignore[attr-defined]
		self._proc = subprocess.Popen(
			args,
			stdout=subprocess.DEVNULL,
			stderr=subprocess.DEVNULL,
			creationflags=creationflags,
			startupinfo=startupinfo,
		)

	def stop(self) -> None:
		if self._proc and self._proc.poll() is None:
			try:
				self._proc.terminate()
			except Exception:
				pass
		try:
			if self._proc:
				self._proc.wait(timeout=3)
		except Exception:
			try:
				if self._proc:
					self._proc.kill()
			except Exception:
				pass
		finally:
			self._proc = None
