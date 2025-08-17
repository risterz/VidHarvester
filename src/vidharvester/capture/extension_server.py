from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Callable, Optional

from vidharvester.utils.logger import get_logger


_log = get_logger("capture.server")


class _CaptureRequestHandler(BaseHTTPRequestHandler):
	"""HTTP handler for POST /capture coming from the browser extension.

	The server instance must set `callback` attribute to a callable that accepts
	`dict` payloads.
	"""

	server: HTTPServer  # type: ignore[assignment]

	def _set_common_headers(self, status: int = 200):
		self.send_response(status)
		self.send_header("Content-Type", "application/json")
		# Allow extension fetches
		self.send_header("Access-Control-Allow-Origin", "*")
		self.send_header("Access-Control-Allow-Headers", "content-type")
		self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
		self.end_headers()

	def do_OPTIONS(self):  # noqa: N802 (method name required by BaseHTTPRequestHandler)
		self._set_common_headers(200)

	def do_POST(self):  # noqa: N802
		if self.path != "/capture":
			self._set_common_headers(404)
			self.wfile.write(b'{"ok": false, "error": "not_found"}')
			return

		length_header = self.headers.get("Content-Length", "0")
		try:
			length = int(length_header)
		except Exception:
			length = 0
		try:
			raw = self.rfile.read(length) if length > 0 else b"{}"
			payload = json.loads(raw.decode("utf-8") or "{}")
		except Exception as exc:
			_log.error("Invalid JSON from extension: %s", exc)
			self._set_common_headers(400)
			self.wfile.write(b'{"ok": false, "error": "bad_json"}')
			return

		url = payload.get("url")
		if not url:
			self._set_common_headers(400)
			self.wfile.write(b'{"ok": false, "error": "missing_url"}')
			return

		callback: Optional[Callable[[dict], None]] = getattr(self.server, "callback", None)
		if callback:
			try:
				callback(payload)
			except Exception as exc:
				_log.exception("Callback error: %s", exc)

		self._set_common_headers(200)
		self.wfile.write(b'{"ok": true}')

	def do_GET(self):  # noqa: N802
		# Health endpoint for quick checks
		if self.path == "/health":
			self._set_common_headers(200)
			self.wfile.write(b'{"ok": true, "status": "healthy"}')
			return
		# Otherwise 404
		self._set_common_headers(404)
		self.wfile.write(b'{"ok": false, "error": "not_found"}')

	def log_message(self, fmt: str, *args):  # quiet default stdout noise
		_log.info("%s - " + fmt, self.client_address[0], *args)


class _Server(HTTPServer):
	def __init__(self, server_address, RequestHandlerClass, callback: Callable[[dict], None]):
		super().__init__(server_address, RequestHandlerClass)
		self.callback = callback


def start_server(port: int, callback: Callable[[dict], None]) -> threading.Thread:
	"""Start the capture HTTP server on 127.0.0.1:`port`.

	Returns the daemon thread running `serve_forever()`.
	"""
	server = _Server(("127.0.0.1", port), _CaptureRequestHandler, callback)
	thread = threading.Thread(target=server.serve_forever, name=f"capture-server:{port}")
	thread.daemon = True
	thread.start()
	_log.info("Capture server listening on http://127.0.0.1:%d/capture", port)
	return thread
