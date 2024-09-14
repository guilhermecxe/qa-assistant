from PySide6.QtWidgets import (
    QLabel, QDialog, QVBoxLayout, QTextEdit)
from PySide6.QtGui import QFont

class ContextDialog(QDialog):
    def __init__(self, question, context):
        super().__init__()

        geometry = self.screen().availableGeometry()
        self.setWindowTitle("Contexto")
        self.setMinimumSize(geometry.width() * 0.4, geometry.height() * 0.7)
        self.setFont(QFont('Segoe UI', 10))

        self.layout = QVBoxLayout()
        self.set_description(question)
        self.set_context(context)

        self.setLayout(self.layout)

    def set_description(self, question):
        self.description = QLabel(
            f'''Para responder ao comando "{question}", '''
            '''levou-se em consideração os seguintes dados:''')
        self.description.setWordWrap(True)
        self.layout.addWidget(self.description)

    def set_context(self, context):
        self.context = QTextEdit()
        self.context.setText(context)
        self.context.setReadOnly(True)
        self.layout.addWidget(self.context)