from PySide6.QtGui import QPainter


class PainterContext:
    def __init__(self, painter: QPainter):
        self.painter = painter

    def __enter__(self):
        # Save the original state of the painter at the beginning of the block
        self.painter.save()
        return self.painter

    def __exit__(self, exc_type, exc_value, traceback):
        # Restore the painter to its original state at the end of the block
        self.painter.restore()
