from __future__ import annotations

import sys

from PyQt6 import QtWidgets, QtCore

from vidharvester.gui.main_window import MainWindow
from vidharvester.gui.theme_manager import ThemeManager
from vidharvester.capture.extension_server import start_server


CAPTURE_PORT = 8089


class CaptureBridge(QtCore.QObject):
	payload_received = QtCore.pyqtSignal(dict)


def main():
	app = QtWidgets.QApplication(sys.argv)
	app.setApplicationName("VidHarvester")

	# Set app/tray icon
	app.setWindowIcon(ThemeManager.build_app_icon("dark"))
	window = MainWindow()
	window.show()

	bridge = CaptureBridge()
	bridge.payload_received.connect(window.on_capture_received)

	# Start local capture server and forward payloads via Qt signal (thread-safe)
	def forward(payload: dict):
		bridge.payload_received.emit(payload)

	start_server(CAPTURE_PORT, forward)

	sys.exit(app.exec())


if __name__ == "__main__":
	main()
