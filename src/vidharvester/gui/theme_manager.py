from __future__ import annotations

from PyQt6 import QtWidgets, QtGui, QtCore


DARK_QSS = """
QWidget { background-color: #121212; color: #eaeaea; }
QLineEdit, QPlainTextEdit, QTreeWidget, QListWidget, QTableWidget { background-color: #1e1e1e; border: 1px solid #2a2a2a; }
QPushButton { background-color: #2a2a2a; border: 1px solid #3a3a3a; padding: 6px 10px; border-radius: 4px; }
QPushButton:hover { background-color: #343434; }
QPushButton:disabled { color: #888888; }
QProgressBar { border: 1px solid #3a3a3a; border-radius: 4px; background: #1e1e1e; }
QProgressBar::chunk { background-color: #4caf50; }
QTabBar::tab { background: #1e1e1e; border: 1px solid #2a2a2a; padding: 6px; }
QTabBar::tab:selected { background: #2a2a2a; }
QMenu { background: #1e1e1e; border: 1px solid #2a2a2a; }
QMenu::item:selected { background: #343434; }
QHeaderView::section { background: #1e1e1e; border: 1px solid #2a2a2a; }
"""

LIGHT_QSS = """
QWidget { background-color: #ffffff; color: #222222; }
QLineEdit, QPlainTextEdit, QTreeWidget, QListWidget, QTableWidget { background-color: #ffffff; border: 1px solid #cccccc; }
QPushButton { background-color: #f2f2f2; border: 1px solid #cccccc; padding: 6px 10px; border-radius: 4px; }
QPushButton:hover { background-color: #e6e6e6; }
QPushButton:disabled { color: #aaaaaa; }
QProgressBar { border: 1px solid #cccccc; border-radius: 4px; background: #f7f7f7; }
QProgressBar::chunk { background-color: #4caf50; }
QTabBar::tab { background: #f7f7f7; border: 1px solid #cccccc; padding: 6px; }
QTabBar::tab:selected { background: #e6e6e6; }
QMenu { background: #ffffff; border: 1px solid #cccccc; }
QMenu::item:selected { background: #e6e6e6; }
QHeaderView::section { background: #f7f7f7; border: 1px solid #cccccc; }
"""


class ThemeManager:
    THEMES = {"dark": DARK_QSS, "light": LIGHT_QSS}

    @classmethod
    def apply_theme(cls, app: QtWidgets.QApplication, theme_name: str) -> None:
        qss = cls.THEMES.get(theme_name, "")
        app.setStyleSheet(qss)

    @classmethod
    def _accent(cls, theme_name: str) -> QtGui.QColor:
        if (theme_name or "dark").lower() == "dark":
            return QtGui.QColor(76, 175, 80)
        return QtGui.QColor(33, 150, 243)

    @classmethod
    def icon(cls, name: str, size: int = 16, theme_name: str | None = None) -> QtGui.QIcon:
        """Create a small, crisp icon drawn on-the-fly to avoid external assets."""
        if theme_name is None:
            # Try to infer from saved style on the app if available
            theme_name = "dark" if (QtWidgets.QApplication.instance() and QtWidgets.QApplication.instance().styleSheet() == DARK_QSS) else "light"
        pm = QtGui.QPixmap(size, size)
        pm.fill(QtCore.Qt.GlobalColor.transparent)
        p = QtGui.QPainter(pm)
        p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        fg = QtGui.QColor("#eaeaea" if (theme_name or "dark").lower() == "dark" else "#222222")
        accent = cls._accent(theme_name)

        def pen(width=2, color=fg):
            qpen = QtGui.QPen(color)
            qpen.setWidth(width)
            qpen.setJoinStyle(QtCore.Qt.PenJoinStyle.RoundJoin)
            qpen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            return qpen

        rect = pm.rect().adjusted(1, 1, -1, -1)

        if name == "download":
            p.setPen(pen(2, accent))
            # Down arrow
            cx, cy = rect.center().x(), rect.center().y()
            p.drawLine(cx, rect.top() + 2, cx, rect.bottom() - 4)
            p.drawLine(cx, rect.bottom() - 4, rect.center().x() - 4, rect.bottom() - 10)
            p.drawLine(cx, rect.bottom() - 4, rect.center().x() + 4, rect.bottom() - 10)
        elif name == "pause":
            p.setPen(pen(0))
            p.setBrush(accent)
            w = max(2, size // 5)
            gap = max(2, size // 6)
            bar_h = rect.height() - 4
            x1 = rect.left() + gap
            x2 = rect.right() - w - gap
            y = rect.top() + 2
            p.drawRoundedRect(QtCore.QRect(x1, y, w, bar_h), 2, 2)
            p.drawRoundedRect(QtCore.QRect(x2, y, w, bar_h), 2, 2)
        elif name == "cancel" or name == "close" or name == "trash":
            color = QtGui.QColor(244, 67, 54) if name != "trash" else fg
            p.setPen(pen(2, color))
            if name == "trash":
                # Simple trash can
                p.drawLine(rect.left() + 3, rect.top() + 4, rect.right() - 3, rect.top() + 4)
                p.drawRect(rect.adjusted(4, 6, -4, -2))
                p.drawLine(rect.center().x(), rect.top() + 8, rect.center().x(), rect.bottom() - 4)
            else:
                p.drawLine(rect.left() + 3, rect.top() + 3, rect.right() - 3, rect.bottom() - 3)
                p.drawLine(rect.right() - 3, rect.top() + 3, rect.left() + 3, rect.bottom() - 3)
        elif name == "settings":
            # Cog: circle + 6 teeth
            p.setPen(pen(2, fg))
            center = rect.center()
            radius = min(rect.width(), rect.height()) // 3
            for i in range(6):
                angle = i * 60
                a = QtCore.QLineF.fromPolar(radius + 3, angle)
                a.translate(center)
                p.drawLine(a.p1(), a.p2())
            p.setBrush(QtGui.QBrush(accent))
            p.drawEllipse(center, radius - 1, radius - 1)
            p.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        elif name == "folder":
            p.setPen(pen(2, fg))
            p.drawRoundedRect(rect.adjusted(1, 4, -1, -2), 2, 2)
            p.drawLine(rect.left() + 3, rect.top() + 5, rect.left() + size // 3, rect.top() + 5)
        elif name == "open":
            p.setPen(pen(2, accent))
            # Northeast arrow
            p.drawLine(rect.left() + 3, rect.bottom() - 3, rect.right() - 3, rect.top() + 3)
            p.drawLine(rect.right() - 3, rect.top() + 3, rect.right() - 6, rect.top() + 3)
            p.drawLine(rect.right() - 3, rect.top() + 3, rect.right() - 3, rect.top() + 6)
        elif name == "search":
            p.setPen(pen(2, fg))
            r = min(rect.width(), rect.height()) // 3
            center = rect.center() - QtCore.QPoint(2, 2)
            p.drawEllipse(center, r, r)
            p.drawLine(center.x() + r, center.y() + r, rect.right() - 2, rect.bottom() - 2)
        elif name == "sun":
            p.setPen(pen(2, QtGui.QColor(255, 193, 7)))
            center = rect.center()
            p.drawEllipse(center, 3, 3)
            for i in range(8):
                a = i * 45
                ray = QtCore.QLineF.fromPolar(size // 3, a)
                ray.translate(center)
                p.drawLine(ray.p1(), ray.p2())
        elif name == "moon":
            p.setPen(pen(0))
            p.setBrush(QtGui.QColor(255, 235, 59))
            cres = QtGui.QPainterPath()
            cres.addEllipse(rect.adjusted(4, 2, -4, -2))
            cut = QtGui.QPainterPath()
            cut.addEllipse(rect.adjusted(7, 2, -1, -2))
            cres = cres.subtracted(cut)
            p.drawPath(cres)
        else:
            # default: simple accent dot
            p.setPen(pen(0))
            p.setBrush(accent)
            p.drawEllipse(rect.center(), 3, 3)

        p.end()
        icon = QtGui.QIcon()
        icon.addPixmap(pm)
        return icon

    @classmethod
    def build_app_icon(cls, theme_name: str | None = None) -> QtGui.QIcon:
        if theme_name is None:
            theme_name = "dark" if (QtWidgets.QApplication.instance() and QtWidgets.QApplication.instance().styleSheet() == DARK_QSS) else "light"
        size = 64
        pm = QtGui.QPixmap(size, size)
        pm.fill(QtCore.Qt.GlobalColor.transparent)
        p = QtGui.QPainter(pm)
        p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        bg = QtGui.QColor(30, 30, 30) if theme_name == "dark" else QtGui.QColor(240, 240, 240)
        accent = cls._accent(theme_name)
        rect = pm.rect().adjusted(2, 2, -2, -2)
        p.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 40)))
        p.setBrush(bg)
        p.drawRoundedRect(rect, 12, 12)
        # Down arrow emblem
        p.setPen(QtGui.QPen(accent, 6, cap=QtCore.Qt.PenCapStyle.RoundCap, join=QtCore.Qt.PenJoinStyle.RoundJoin))
        cx, cy = rect.center().x(), rect.center().y()
        p.drawLine(cx, cy - 12, cx, cy + 10)
        p.drawLine(cx, cy + 10, cx - 10, cy)
        p.drawLine(cx, cy + 10, cx + 10, cy)
        p.end()
        icon = QtGui.QIcon()
        icon.addPixmap(pm)
        return icon
