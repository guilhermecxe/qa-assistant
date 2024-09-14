from PySide6.QtWidgets import QTextEdit

class QuestionManager():
    def __init__(self, question:QTextEdit):
        self.question = question

    def get_question(self):
        return self.question.toPlainText().strip()
