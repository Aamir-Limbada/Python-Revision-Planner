import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel


class RevisionApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CS Revision Tracker")
        self.setMinimumSize(900, 600)

        title = QLabel("CS Revision Tracker")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")

        self.setCentralWidget(title)


app = QApplication(sys.argv)

window = RevisionApp()
window.show()

sys.exit(app.exec())