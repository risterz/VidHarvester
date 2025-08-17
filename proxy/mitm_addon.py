from mitmproxy import http
import re
import requests

LOCAL_API = "http://127.0.0.1:8089/capture"


class MediaDetector:
	def response(self, flow: http.HTTPFlow) -> None:
		ct = flow.response.headers.get("Content-Type", "")
		url = flow.request.pretty_url
		if (
			("video" in ct)
			or ("application/vnd.apple.mpegurl" in ct)
			or ("application/dash+xml" in ct)
			or re.search(r"\.m3u8|\.mpd|\.mp4|\.webm", url, re.I)
		):
			payload = {"url": url, "page_url": flow.request.headers.get("Referer")}
			try:
				requests.post(LOCAL_API, json=payload, timeout=2)
			except Exception:
				pass


addons = [MediaDetector()]
