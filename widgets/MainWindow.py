from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow

from ui.Ui_MainWindow import Ui_MainWindow


class MainWindow(QMainWindow):
    """
    Main window of an application
    """

    def __init__(self):
        super().__init__()

        # Setup UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.snake_game_widget.score_changed.connect(self.handle_score_changed)

    @Slot(int)
    def handle_score_changed(self, score: int):
        self.ui.score_lcd.display(score)
