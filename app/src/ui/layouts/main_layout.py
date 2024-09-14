from PySide6.QtWidgets import QHBoxLayout, QSpacerItem, QSizePolicy

class MainLayout(QHBoxLayout):
    def __init__(self):
        super().__init__()

        self.setStretch(0, 6)
        self.setStretch(2, 4)
