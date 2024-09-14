import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
import os

from src.ui.main_window import MainWindow

os.environ['REQUESTS_CA_BUNDLE'] = '_internal\\certifi\\cacert.pem'

if __name__ == '__main__':
    app = QApplication()
    app.setWindowIcon(QIcon('resources\\images\\logo-fapeg.ico'))
    window = MainWindow()
    window.show()

    sys.exit(app.exec())