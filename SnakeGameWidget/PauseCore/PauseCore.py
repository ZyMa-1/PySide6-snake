from PySide6.QtCore import QObject, Slot, Qt
from PySide6.QtGui import QFontMetrics, QFont
from PySide6.QtWidgets import QWidget, QPushButton

from SnakeGameWidget.SnakeCore.SnakeCore import SnakeCore


# On hover, oh hold, colors
#
class PauseCore(QObject):
    def __init__(self, parent=None, *, widget: QWidget, snake_core: SnakeCore):
        super().__init__(parent)

        self.snake_core = snake_core
        self.widget = widget

        # QButton here
        self.pause_button = QPushButton('Pause', widget)
        self.pause_button.clicked.connect(self.toggle_pause)

        self.is_paused = False

        self._update_button_geometry()
        widget.installEventFilter(self)

    @Slot()
    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.snake_core.pause_game()
            self.pause_button.setText('Resume')
        else:
            self.snake_core.unpause_game()
            self.pause_button.setText('Pause')

    def eventFilter(self, obj, event):
        if obj == self.pause_button.parent() and event.type() == event.Resize:
            # Update the button's geometry when the parent widget is resized
            self._update_button_geometry()
        return super().eventFilter(obj, event)

    def _update_button_geometry(self):
        button_font = QFont("Arial", int(self.widget.height() / 100 * 20))
        self.pause_button.setFont(button_font)

        font_metrics = QFontMetrics(self.pause_button.font())
        text_size = font_metrics.size(Qt.TextFlag.TextSingleLine, self.pause_button.text(), tabstops=0)

        # Set the fixed top-right corner position and the calculated size
        top_right_x = int(self.widget.height() / 100 * 5)
        top_right_y = int(self.widget.height() / 100 * 5)

        self.pause_button.setGeometry(
            top_right_x - text_size.width(), top_right_y, text_size.width(), text_size.height()
        )
