from PySide6.QtWidgets import QTableWidget, QSizePolicy

class TableWidget(QTableWidget):
    def __init__(self):
        super().__init__()

        self = QTableWidget()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.horizontalHeader().setStretchLastSection(True)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setSelectionMode(QTableWidget.MultiSelection)