from __future__ import annotations

import os
from typing import Optional

from PyQt6 import QtCore, QtGui, QtWidgets

from vidharvester.download.worker import DownloadWorker, DownloadOptions
from vidharvester.database.manager import DatabaseManager
from vidharvester.gui.settings_dialog import SettingsDialog
from vidharvester.gui.system_tray import SystemTrayManager
from vidharvester.capture.proxy_controller import ProxyController
from vidharvester.download.queue_runner import QueueRunner
from vidharvester.gui.theme_manager import ThemeManager
from vidharvester.gui.animated_progress import AnimatedProgressBar


def human_size(n_bytes: Optional[float]) -> str:
    if n_bytes is None:
        return "?"
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    v = float(n_bytes)
    while v >= 1024 and i < len(units) - 1:
        v /= 1024.0
        i += 1
    if i == 0:
        return f"{int(v)} {units[i]}"
    return f"{v:.1f} {units[i]}"


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VidHarvester")
        self.setMinimumSize(1000, 680)
        self.setAcceptDrops(True)

        self.worker: Optional[DownloadWorker] = None
        self.db = DatabaseManager()

        self._build_ui()
        self.tray = SystemTrayManager(self)
        self.proxy = ProxyController()
        self.tray.toggle_capture_action.triggered.connect(self.on_toggle_proxy)
        self.tray.quit_action.triggered.connect(self.close)
        self.queue_runner = QueueRunner(self.db, self)
        self.queue_runner.log.connect(self.append_log)
        self.queue_runner.started.connect(lambda qid: self._refresh_queue_ui())
        self.queue_runner.finished.connect(lambda qid, ok: (self._refresh_queue_ui(), self._refresh_history_ui()))

        self.apply_theme()
        self._refresh_queue_ui()
        self._refresh_history_ui()

    def _build_ui(self):
        widget = QtWidgets.QWidget()
        self.setCentralWidget(widget)
        layout = QtWidgets.QVBoxLayout(widget)

        # Top input area
        input_frame = QtWidgets.QFrame()
        input_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        input_layout = QtWidgets.QHBoxLayout(input_frame)

        self.url_edit = QtWidgets.QLineEdit()
        self.url_edit.setPlaceholderText("Paste URL or drag & drop here...")
        self.url_edit.returnPressed.connect(self.on_download)

        self.download_btn = QtWidgets.QPushButton("Download")
        self.download_btn.clicked.connect(self.on_download)

        self.formats_btn = QtWidgets.QPushButton("Get Info / Formats")
        self.formats_btn.clicked.connect(self.on_get_formats)

        self.pause_btn = QtWidgets.QPushButton("Pause")
        self.pause_btn.clicked.connect(self.on_pause)
        self.pause_btn.setEnabled(False)

        input_layout.addWidget(self.url_edit)
        input_layout.addWidget(self.formats_btn)
        input_layout.addWidget(self.download_btn)
        input_layout.addWidget(self.pause_btn)

        # Options area
        options_frame = QtWidgets.QFrame()
        options_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        options_layout = QtWidgets.QHBoxLayout(options_frame)

        self.mode_combo = QtWidgets.QComboBox()
        self.mode_combo.addItems(["Video", "Audio"])

        self.format_combo = QtWidgets.QComboBox()
        self.format_combo.addItems(["mp4", "webm", "mkv"])

        self.quality_combo = QtWidgets.QComboBox()
        self.quality_combo.addItems(["auto-best", "720p", "1080p", "highest"])

        self.cookies_btn = QtWidgets.QPushButton("Browse Cookies...")
        self.cookies_btn.clicked.connect(self.browse_cookies)
        self.cookies_path: Optional[str] = None

        self.embed_subs_cb = QtWidgets.QCheckBox("Embed Subtitles")
        self.embed_thumb_cb = QtWidgets.QCheckBox("Embed Thumbnail")

        options_layout.addWidget(QtWidgets.QLabel("Mode:"))
        options_layout.addWidget(self.mode_combo)
        options_layout.addWidget(QtWidgets.QLabel("Format:"))
        options_layout.addWidget(self.format_combo)
        options_layout.addWidget(QtWidgets.QLabel("Quality:"))
        options_layout.addWidget(self.quality_combo)
        options_layout.addWidget(self.cookies_btn)
        options_layout.addWidget(self.embed_subs_cb)
        options_layout.addWidget(self.embed_thumb_cb)
        options_layout.addStretch()

        # Update format combo when mode changes
        self.mode_combo.currentTextChanged.connect(self._update_format_options)
        self._update_format_options()

        # Progress area
        progress_frame = QtWidgets.QFrame()
        progress_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        progress_layout = QtWidgets.QVBoxLayout(progress_frame)

        self.progress_bar = AnimatedProgressBar()
        self.status_label = QtWidgets.QLabel("Ready")

        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.status_label)

        # Main content tabs
        self.tabs = QtWidgets.QTabWidget()

        # Captured URLs tab
        self.captured_list = QtWidgets.QListWidget()
        self.captured_list.itemDoubleClicked.connect(self.on_captured_item_clicked)
        self.tabs.addTab(self.captured_list, "Captured")

        # Queue tab
        self.queue_table = QtWidgets.QTableWidget()
        self.queue_table.setColumnCount(6)
        self.queue_table.setHorizontalHeaderLabels(["URL", "Status", "Progress", "Speed", "ETA", "Title"])
        self.queue_table.horizontalHeader().setStretchLastSection(True)
        self.tabs.addTab(self.queue_table, "Queue")

        # History tab
        self.history_table = QtWidgets.QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["Title", "URL", "Format", "Size", "Completed"])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.tabs.addTab(self.history_table, "History")

        # Log tab
        self.log_text = QtWidgets.QPlainTextEdit()
        self.log_text.setMaximumBlockCount(1000)
        self.log_text.setReadOnly(True)
        self.tabs.addTab(self.log_text, "Log")

        # Add everything to main layout
        layout.addWidget(input_frame)
        layout.addWidget(options_frame)
        layout.addWidget(progress_frame)
        layout.addWidget(self.tabs, 1)

        # Menu bar
        self._create_menu_bar()

    def _create_menu_bar(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")
        settings_action = file_menu.addAction("Settings...")
        settings_action.triggered.connect(self.show_settings)
        file_menu.addSeparator()
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)

        # Theme menu
        theme_menu = menubar.addMenu("&Theme")
        dark_action = theme_menu.addAction("Dark")
        dark_action.triggered.connect(lambda: self.set_theme("dark"))
        light_action = theme_menu.addAction("Light")
        light_action.triggered.connect(lambda: self.set_theme("light"))

        # Help menu
        help_menu = menubar.addMenu("&Help")
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about)

    def _update_format_options(self):
        mode = self.mode_combo.currentText().lower()
        self.format_combo.clear()
        if mode == "video":
            self.format_combo.addItems(["mp4", "webm", "mkv"])
        else:  # audio
            self.format_combo.addItems(["mp3", "m4a", "ogg", "flac"])

    def apply_theme(self):
        theme_name = self.db.get_setting("theme", "dark")
        ThemeManager.apply_theme(QtWidgets.QApplication.instance(), theme_name)

    def set_theme(self, theme_name: str):
        self.db.set_setting("theme", theme_name)
        self.apply_theme()

    def show_settings(self):
        dialog = SettingsDialog(self.db, self)
        dialog.exec()

    def show_about(self):
        QtWidgets.QMessageBox.about(
            self,
            "About VidHarvester",
            "VidHarvester v0.1.0\n\nA comprehensive video downloading application with PyQt6 GUI, browser extension integration, and proxy-based video capture capabilities."
        )

    def browse_cookies(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select Cookies File", "", "Text Files (*.txt);;All Files (*)"
        )
        if path:
            self.cookies_path = path
            self.cookies_btn.setText(f"Cookies: {os.path.basename(path)}")
        else:
            self.cookies_path = None
            self.cookies_btn.setText("Browse Cookies...")

    def on_capture_received(self, payload: dict):
        """Called when extension/proxy captures a URL."""
        url = payload.get("url", "")
        if url:
            item = QtWidgets.QListWidgetItem(url)
            self.captured_list.insertItem(0, item)
            self.tabs.setCurrentWidget(self.captured_list)
            self.tray.show_message("URL Captured", f"Captured: {url[:50]}...")

    def on_captured_item_clicked(self, item):
        """Double-click on captured URL to load it."""
        self.url_edit.setText(item.text())
        self.tabs.setCurrentIndex(0)  # Switch to first tab

    def on_get_formats(self):
        """Get available formats for the URL."""
        url = self.url_edit.text().strip()
        if not url:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please enter a URL first.")
            return

        self.append_log(f"[info] Getting formats for: {url}")
        # This would typically show a dialog with available formats
        # For now, just log the action
        QtWidgets.QMessageBox.information(self, "Info", "Format detection would be implemented here.")

    def on_download(self):
        """Start download."""
        url = self.url_edit.text().strip()
        if not url:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please enter a URL first.")
            return

        if self.worker and self.worker.isRunning():
            QtWidgets.QMessageBox.warning(self, "Warning", "A download is already in progress.")
            return

        # Get output directory
        output_dir = self.db.get_setting("output_directory", "")
        if not output_dir:
            output_dir = QtCore.QStandardPaths.standardLocations(
                QtCore.QStandardPaths.StandardLocation.DownloadLocation
            )[0]

        options = DownloadOptions(
            output_directory=output_dir,
            mode=self.mode_combo.currentText().lower(),
            format_str=self.format_combo.currentText(),
            quality=self.quality_combo.currentText(),
            filename_template="%(title)s.%(ext)s",
            embed_subtitles=self.embed_subs_cb.isChecked(),
            embed_thumbnail=self.embed_thumb_cb.isChecked(),
            cookies_file=self.cookies_path
        )

        self.worker = DownloadWorker(url, options)
        self.worker.progress_signal.connect(self.on_progress)
        self.worker.log_signal.connect(self.append_log)
        self.worker.finished_signal.connect(self.on_download_finished)

        self.download_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.progress_bar.setAnimated(True)
        self.status_label.setText("Starting download...")

        self.worker.start()
        self.tabs.setCurrentWidget(self.log_text)

    def on_pause(self):
        """Pause/stop download."""
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.append_log("[info] Download canceled by user.")

    def on_progress(self, data: dict):
        """Handle download progress updates."""
        status = data.get("status", "")
        if status == "downloading":
            percent = data.get("percent")
            if percent is not None:
                self.progress_bar.setValue(percent)
            
            speed = data.get("speed")
            eta = data.get("eta")
            filename = data.get("filename", "")
            
            status_parts = []
            if filename:
                status_parts.append(f"File: {os.path.basename(filename)}")
            if speed:
                status_parts.append(f"Speed: {human_size(speed)}/s")
            if eta:
                status_parts.append(f"ETA: {eta}s")
            
            self.status_label.setText(" | ".join(status_parts) if status_parts else "Downloading...")

        elif status == "finished":
            self.progress_bar.setValue(100)
            self.status_label.setText("Download completed!")

    def on_download_finished(self, success: bool, message: str):
        """Handle download completion."""
        self.download_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.progress_bar.setAnimated(False)
        
        if success:
            self.progress_bar.setValue(100)
            self.status_label.setText("Download completed!")
            self.append_log(f"[success] {message}")
        else:
            self.progress_bar.setValue(0)
            self.status_label.setText("Download failed!")
            self.append_log(f"[error] {message}")

        self.worker = None
        self._refresh_history_ui()

    def on_toggle_proxy(self):
        """Toggle proxy capture on/off."""
        if self.proxy.is_running():
            self.proxy.stop()
            self.tray.toggle_capture_action.setText("Start Capture")
            self.append_log("[info] Proxy capture stopped.")
        else:
            try:
                self.proxy.start()
                self.tray.toggle_capture_action.setText("Stop Capture")
                self.append_log("[info] Proxy capture started on port 8080.")
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Error", f"Failed to start proxy: {e}")

    def append_log(self, message: str):
        """Add message to log."""
        self.log_text.appendPlainText(message)

    def _refresh_queue_ui(self):
        """Refresh the queue table."""
        queue_items = self.db.fetch_queue()
        self.queue_table.setRowCount(len(queue_items))
        
        for row, item in enumerate(queue_items):
            self.queue_table.setItem(row, 0, QtWidgets.QTableWidgetItem(item["url"][:50] + "..."))
            self.queue_table.setItem(row, 1, QtWidgets.QTableWidgetItem(item["status"]))
            
            progress = item["progress"]
            progress_text = f"{progress:.1f}%" if progress else "-"
            self.queue_table.setItem(row, 2, QtWidgets.QTableWidgetItem(progress_text))
            
            speed = item["speed"]
            speed_text = f"{human_size(speed)}/s" if speed else "-"
            self.queue_table.setItem(row, 3, QtWidgets.QTableWidgetItem(speed_text))
            
            eta = item["eta"]
            eta_text = f"{eta}s" if eta else "-"
            self.queue_table.setItem(row, 4, QtWidgets.QTableWidgetItem(eta_text))
            
            title = item["title"] or "Unknown"
            self.queue_table.setItem(row, 5, QtWidgets.QTableWidgetItem(title))

    def _refresh_history_ui(self):
        """Refresh the history table."""
        history_items = self.db.fetch_history()
        self.history_table.setRowCount(len(history_items))
        
        for row, item in enumerate(history_items):
            title = item["title"] or "Unknown"
            self.history_table.setItem(row, 0, QtWidgets.QTableWidgetItem(title))
            self.history_table.setItem(row, 1, QtWidgets.QTableWidgetItem(item["url"][:50] + "..."))
            self.history_table.setItem(row, 2, QtWidgets.QTableWidgetItem(item["format"] or "-"))
            
            size = item["size_bytes"]
            size_text = human_size(size) if size else "-"
            self.history_table.setItem(row, 3, QtWidgets.QTableWidgetItem(size_text))
            
            self.history_table.setItem(row, 4, QtWidgets.QTableWidgetItem(item["completed_at"]))

    def dragEnterEvent(self, event):
        """Handle drag enter for URLs."""
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        """Handle URL drop."""
        text = event.mimeData().text().strip()
        if text.startswith(("http://", "https://")):
            self.url_edit.setText(text)
            event.acceptProposedAction()

    def closeEvent(self, event):
        """Handle window close."""
        if self.worker and self.worker.isRunning():
            reply = QtWidgets.QMessageBox.question(
                self, "Confirm Exit",
                "A download is in progress. Are you sure you want to exit?",
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
                QtWidgets.QMessageBox.StandardButton.No
            )
            if reply == QtWidgets.QMessageBox.StandardButton.No:
                event.ignore()
                return
            self.worker.stop()

        if self.proxy.is_running():
            self.proxy.stop()
        
        super().closeEvent(event)