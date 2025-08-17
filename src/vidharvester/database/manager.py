from __future__ import annotations

import os
import sqlite3
import threading
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional, Tuple


def _app_data_dir() -> str:
	base = os.getenv("APPDATA") or os.path.join(os.path.expanduser("~"), ".local", "share")
	path = os.path.join(base, "VidHarvester")
	os.makedirs(path, exist_ok=True)
	return path


def default_db_path() -> str:
	return os.path.join(_app_data_dir(), "vidharvester.db")


class DatabaseManager:
	"""Thread-safe SQLite wrapper for settings, queue, and history."""

	def __init__(self, db_path: Optional[str] = None) -> None:
		self.db_path = db_path or default_db_path()
		self._lock = threading.RLock()
		self._init()

	def _connect(self) -> sqlite3.Connection:
		conn = sqlite3.connect(self.db_path, check_same_thread=False)
		conn.row_factory = sqlite3.Row
		return conn

	def _init(self) -> None:
		with self._connect() as con:
			cur = con.cursor()
			cur.executescript(
				"""
				CREATE TABLE IF NOT EXISTS settings (
					key TEXT PRIMARY KEY,
					value TEXT
				);

				CREATE TABLE IF NOT EXISTS queue (
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					url TEXT NOT NULL,
					mode TEXT NOT NULL,
					format TEXT NOT NULL,
					quality TEXT NOT NULL,
					output_dir TEXT NOT NULL,
					filename_template TEXT NOT NULL,
					status TEXT NOT NULL DEFAULT 'pending',
					progress REAL,
					speed REAL,
					eta INTEGER,
					title TEXT,
					created_at TEXT NOT NULL,
					started_at TEXT,
					finished_at TEXT
				);

				CREATE TABLE IF NOT EXISTS history (
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					url TEXT NOT NULL,
					output_path TEXT,
					title TEXT,
					format TEXT,
					size_bytes INTEGER,
					source TEXT,
					completed_at TEXT NOT NULL
				);
				"""
			)
			con.commit()

	# Settings
	def get_setting(self, key: str, default: Optional[str] = None) -> Optional[str]:
		with self._connect() as con:
			row = con.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
			return row[0] if row else default

	def set_setting(self, key: str, value: str) -> None:
		with self._connect() as con:
			con.execute("REPLACE INTO settings(key, value) VALUES(?, ?)", (key, value))
			con.commit()

	# Queue
	def add_queue_item(self, item: Dict[str, Any]) -> int:
		with self._connect() as con:
			cur = con.execute(
				"""
				INSERT INTO queue(url, mode, format, quality, output_dir, filename_template, status, created_at)
				VALUES(?, ?, ?, ?, ?, ?, 'pending', ?)
				""",
				(
					item["url"],
					item["mode"],
					item["format"],
					item["quality"],
					item["output_dir"],
					item["filename_template"],
					datetime.utcnow().isoformat(),
				),
			)
			con.commit()
			return int(cur.lastrowid)

	def update_queue_progress(self, qid: int, progress: Optional[float], speed: Optional[float], eta: Optional[int]) -> None:
		with self._connect() as con:
			con.execute(
				"UPDATE queue SET progress=?, speed=?, eta=? WHERE id=?",
				(progress, speed, eta, qid),
			)
			con.commit()

	def set_queue_status(self, qid: int, status: str, title: Optional[str] = None) -> None:
		fields = ["status=?"]
		params: List[Any] = [status]
		if status == "running":
			fields.append("started_at=?")
			params.append(datetime.utcnow().isoformat())
		if status in ("completed", "failed", "canceled"):
			fields.append("finished_at=?")
			params.append(datetime.utcnow().isoformat())
		if title is not None:
			fields.append("title=?")
			params.append(title)
		params.append(qid)
		with self._connect() as con:
			con.execute(f"UPDATE queue SET {', '.join(fields)} WHERE id=?", tuple(params))
			con.commit()

	def fetch_queue(self, statuses: Optional[Iterable[str]] = None) -> List[sqlite3.Row]:
		with self._connect() as con:
			if statuses:
				qmarks = ",".join(["?"] * len(list(statuses)))
				return list(con.execute(f"SELECT * FROM queue WHERE status IN ({qmarks}) ORDER BY id", tuple(statuses)))
			return list(con.execute("SELECT * FROM queue ORDER BY id"))

	def get_queue_item(self, qid: int) -> Optional[sqlite3.Row]:
		with self._connect() as con:
			row = con.execute("SELECT * FROM queue WHERE id=?", (qid,)).fetchone()
			return row

	def delete_queue_item(self, qid: int) -> None:
		with self._connect() as con:
			con.execute("DELETE FROM queue WHERE id=?", (qid,))
			con.commit()

	# History
	def add_history(self, url: str, output_path: Optional[str], title: Optional[str], fmt: Optional[str], size_bytes: Optional[int], source: Optional[str]) -> None:
		with self._connect() as con:
			con.execute(
				"""
				INSERT INTO history(url, output_path, title, format, size_bytes, source, completed_at)
				VALUES(?, ?, ?, ?, ?, ?, ?)
				""",
				(url, output_path, title, fmt, size_bytes, source, datetime.utcnow().isoformat()),
			)
			con.commit()

	def fetch_history(self, limit: int = 200) -> List[sqlite3.Row]:
		with self._connect() as con:
			return list(con.execute("SELECT * FROM history ORDER BY id DESC LIMIT ?", (limit,)))
