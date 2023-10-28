import sys

from PySide6.QtWidgets import QApplication

from widgets.MainWindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setOrganizationName("ZyMa-1")
    app.setApplicationName("Snake game")
    app.setApplicationVersion("2.0")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
