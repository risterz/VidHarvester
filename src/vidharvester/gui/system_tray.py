from __future__ import annotations

from PyQt6 import QtCore, QtGui, QtWidgets

from vidharvester.gui.theme_manager import ThemeManager


class SystemTrayManager(QtCore.QObject):
    """Manages system tray icon and context menu."""
    
    def __init__(self, parent_window: QtWidgets.QMainWindow):
        super().__init__(parent_window)
        self.parent_window = parent_window
        
        if not QtWidgets.QSystemTrayIcon.isSystemTrayAvailable():
            return
            
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self.tray_icon.setIcon(ThemeManager.build_app_icon("dark"))
        
        # Context menu
        menu = QtWidgets.QMenu()
        
        self.toggle_capture_action = menu.addAction("Start Capture")
        menu.addSeparator()
        self.quit_action = menu.addAction("Quit")
        
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.activated.connect(self._on_activated)
        self.tray_icon.show()
        
    def _on_activated(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.ActivationReason.DoubleClick:
            self.parent_window.show()
            self.parent_window.raise_()
            self.parent_window.activateWindow()
            
    def show_message(self, title: str, message: str):
        """Show a system tray notification."""
        if hasattr(self, 'tray_icon'):
            self.tray_icon.showMessage(title, message, QtWidgets.QSystemTrayIcon.MessageIcon.Information, 3000)
