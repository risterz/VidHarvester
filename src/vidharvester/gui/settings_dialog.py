from __future__ import annotations

from PyQt6 import QtCore, QtWidgets

from vidharvester.database.manager import DatabaseManager


class SettingsDialog(QtWidgets.QDialog):
    """Settings dialog for VidHarvester configuration."""
    
    def __init__(self, db: DatabaseManager, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.setMinimumWidth(400)
        
        self._build_ui()
        self._load_settings()
        
    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        
        # Output folder
        folder_group = QtWidgets.QGroupBox("Output")
        folder_layout = QtWidgets.QVBoxLayout(folder_group)
        
        folder_row = QtWidgets.QHBoxLayout()
        self.folder_edit = QtWidgets.QLineEdit()
        folder_browse = QtWidgets.QPushButton("Browse...")
        folder_browse.clicked.connect(self._browse_folder)
        folder_row.addWidget(self.folder_edit)
        folder_row.addWidget(folder_browse)
        folder_layout.addLayout(folder_row)
        
        # Max concurrent downloads
        concurrent_group = QtWidgets.QGroupBox("Downloads")
        concurrent_layout = QtWidgets.QFormLayout(concurrent_group)
        
        self.concurrent_spin = QtWidgets.QSpinBox()
        self.concurrent_spin.setMinimum(1)
        self.concurrent_spin.setMaximum(10)
        self.concurrent_spin.setValue(2)
        concurrent_layout.addRow("Max concurrent downloads:", self.concurrent_spin)
        
        # Buttons
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok |
            QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self._save_and_accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(folder_group)
        layout.addWidget(concurrent_group)
        layout.addWidget(button_box)
        
    def _browse_folder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Output Directory", self.folder_edit.text()
        )
        if folder:
            self.folder_edit.setText(folder)
            
    def _load_settings(self):
        output_dir = self.db.get_setting("output_directory", "")
        if not output_dir:
            output_dir = QtCore.QStandardPaths.standardLocations(
                QtCore.QStandardPaths.StandardLocation.DownloadLocation
            )[0]
        self.folder_edit.setText(output_dir)
        
        max_concurrent = int(self.db.get_setting("max_concurrent_downloads", "2") or "2")
        self.concurrent_spin.setValue(max_concurrent)
        
    def _save_and_accept(self):
        self.db.set_setting("output_directory", self.folder_edit.text())
        self.db.set_setting("max_concurrent_downloads", str(self.concurrent_spin.value()))
        self.accept()
