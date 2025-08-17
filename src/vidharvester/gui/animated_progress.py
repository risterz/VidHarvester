from __future__ import annotations

import math
from typing import Optional

from PyQt6 import QtCore, QtGui, QtWidgets


class AnimatedProgressBar(QtWidgets.QWidget):
    """Custom progress bar with animated diagonal stripes."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(20)
        self.setMinimumWidth(200)
        
        self._value = 0.0  # 0.0 to 100.0
        self._animated = False
        self._offset = 0
        
        # Animation timer
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._animate)
        self._timer.setInterval(50)  # 20 FPS
        
    def setValue(self, value: float):
        """Set progress value (0.0 to 100.0)."""
        self._value = max(0.0, min(100.0, value))
        self.update()
        
    def setAnimated(self, animated: bool):
        """Enable/disable animation."""
        self._animated = animated
        if animated:
            self._timer.start()
        else:
            self._timer.stop()
        self.update()
        
    def _animate(self):
        """Animation step."""
        self._offset = (self._offset + 1) % 20
        self.update()
        
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        
        rect = self.rect()
        
        # Background
        painter.fillRect(rect, QtGui.QColor(40, 40, 40))
        
        # Progress bar
        if self._value > 0:
            progress_width = int(rect.width() * self._value / 100.0)
            progress_rect = QtCore.QRect(0, 0, progress_width, rect.height())
            
            # Base color
            base_color = QtGui.QColor(70, 130, 200)
            painter.fillRect(progress_rect, base_color)
            
            # Animated stripes if enabled
            if self._animated:
                stripe_color = QtGui.QColor(90, 150, 220, 100)
                painter.fillRect(progress_rect, stripe_color)
                
                # Draw diagonal stripes
                painter.setPen(QtGui.QPen(QtGui.QColor(110, 170, 240, 150), 1))
                for x in range(-20, progress_width + 20, 10):
                    line_x = x + self._offset
                    painter.drawLine(line_x, 0, line_x + rect.height(), rect.height())
        
        # Border
        painter.setPen(QtGui.QPen(QtGui.QColor(60, 60, 60), 1))
        painter.drawRect(rect.adjusted(0, 0, -1, -1))
