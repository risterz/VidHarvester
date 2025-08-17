from __future__ import annotations

from typing import Optional

from PyQt6 import QtCore

from vidharvester.database.manager import DatabaseManager
from vidharvester.download.worker import DownloadWorker, DownloadOptions


class QueueRunner(QtCore.QObject):
	"""Simple queue runner that auto-starts pending items up to a concurrency limit."""

	started = QtCore.pyqtSignal(int)
	finished = QtCore.pyqtSignal(int, bool)
	log = QtCore.pyqtSignal(str)

	def __init__(self, db: DatabaseManager, parent=None):
		super().__init__(parent)
		self.db = db
		self.max_concurrent = int(self.db.get_setting("max_concurrent_downloads", "2") or "2")
		self._active: dict[int, DownloadWorker] = {}
		self._timer = QtCore.QTimer(self)
		self._timer.setInterval(1000)
		self._timer.timeout.connect(self._tick)
		self._timer.start()

	def _tick(self):
		# Refresh max_concurrent in case settings changed
		try:
			self.max_concurrent = int(self.db.get_setting("max_concurrent_downloads", "2") or "2")
		except Exception:
			self.max_concurrent = 2
		# Start new tasks if below limit
		if len(self._active) >= self.max_concurrent:
			return
		pending = [r for r in self.db.fetch_queue(["pending"])][:max(0, self.max_concurrent - len(self._active))]
		for r in pending:
			self._start_row(r)

	def _start_row(self, row):
		qid = int(row["id"])
		options = DownloadOptions(
			output_directory=row["output_dir"],
			mode=row["mode"],
			format_str=row["format"],
			quality=row["quality"],
			filename_template=row["filename_template"],
		)
		w = DownloadWorker(url=row["url"], options=options)
		w.log_signal.connect(self.log)
		w.finished_signal.connect(lambda success, msg, qid=qid, w=w, url=row["url"]: self._on_finished(qid, success, w, url))
		w.progress_signal.connect(lambda d, qid=qid: self._on_progress(qid, d))
		self._active[qid] = w
		self.db.set_queue_status(qid, "running")
		self.started.emit(qid)
		w.start()

	def _on_progress(self, qid: int, d: dict):
		if d.get("status") == "downloading":
			self.db.update_queue_progress(qid, d.get("percent"), d.get("speed"), d.get("eta"))

	def _on_finished(self, qid: int, success: bool, worker: Optional[DownloadWorker] = None, url: Optional[str] = None):
		self.db.set_queue_status(qid, "completed" if success else "failed")
		w = self._active.pop(qid, None)
		# Add to history for queue-runner initiated tasks
		try:
			if success and worker is not None:
				self.db.add_history(
					url or "",
					getattr(worker, "last_filename", None),
					getattr(worker, "last_title", None),
					getattr(worker, "last_format", None),
					getattr(worker, "last_size", None),
					"queue",
				)
		except Exception:
			pass
		self.finished.emit(qid, success)
