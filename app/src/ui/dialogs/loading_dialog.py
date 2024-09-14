from PySide6.QtWidgets import (
    QLabel, QDialog, QVBoxLayout)
from PySide6.QtGui import QMovie
from PySide6.QtCore import Qt

class LoadingDialog(QDialog):
    def __init__(self, description):
        super().__init__()
        self.setWindowTitle("Carregando...")
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.setFixedSize(350, 120)

        self.layout = QVBoxLayout()
        
        self.set_description(description)
        self.set_loading_label()
        self.layout.addWidget(QLabel('Por favor, aguarde...', alignment=Qt.AlignCenter))

        self.setLayout(self.layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape: # inpedindo que o usuário use 'Esc' para fechar a janela
            event.ignore()
        else:
            super().keyPressEvent(event)

    def set_description(self, description):
        self.description = QLabel(description)
        self.description.setContentsMargins(0, 0, 0, 10)
        self.layout.addWidget(self.description, alignment=Qt.AlignCenter)

    def set_loading_label(self):
        self.loading_label = QLabel(self)
        movie = QMovie("resources\\images\\duck-loading.gif")
        self.loading_label.setFixedSize(50, 50)
        self.loading_label.setMovie(movie)
        movie.start()
        self.layout.addWidget(self.loading_label, alignment=Qt.AlignCenter)

