from PySide6.QtWidgets import QTextEdit

class QuestionTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setMaximumHeight(100)

class AnswearTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)