from PySide6.QtCore import QObject
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import QWidget

from .PauseCore import PauseCore


class PausePainter(QObject):
    """
    Class for painting pause message over the game screen.
    """

    def __init__(self, parent=None, *, widget: QWidget, pause_core: PauseCore):
        super().__init__(parent)

        self.widget = widget
        self.pause_core = pause_core

    def paint(self, painter: QPainter):
        if not self.pause_core.is_paused:
            return

        painter.save()

        # Black overlay
        painter.setOpacity(0.2)
        painter.fillRect(self.widget.rect(), QColor(0, 0, 0))

        # Pause indicator
        painter.restore()
        widget_width = self.widget.width()
        widget_height = self.widget.height()
        line_x1 = int(widget_width - widget_width * 0.1)
        line_x2 = int(widget_width - widget_width * 0.05)
        line_y = int(widget_height * 0.08)
        line_thickness = int(widget_height * 0.03)

        line_color = QColor(0, 0, 0)

        pen = QPen(line_color)
        pen.setWidthF(line_thickness)
        painter.setPen(pen)

        # Draw two parallel vertical lines
        painter.drawLine(line_x1, line_y, line_x1, line_y + line_thickness * 2)
        painter.drawLine(line_x2, line_y, line_x2, line_y + line_thickness * 2)

        painter.restore()
