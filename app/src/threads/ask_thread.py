from rag import Assistant
from PySide6.QtCore import QThread, Signal

class AskWorkerThread(QThread):
    result_ready = Signal(str)

    def __init__(self, ai:Assistant, question_text, files):
        super().__init__()
        self.ai = ai
        self.question_text = question_text
        self.files = files

    def run(self):
        answear = self.ai.ask(self.question_text, self.files if self.files else {})
        # answear = '<answear>'
        # time.sleep(10)
        self.result_ready.emit(answear)