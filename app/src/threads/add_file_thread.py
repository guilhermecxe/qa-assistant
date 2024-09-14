from PySide6.QtCore import QThread, Signal
import rag

class AddFileWorkerThread(QThread):
    result_ready = Signal()

    def __init__(self, ai:rag.Assistant, file_path):
        super().__init__()
        self.ai = ai
        self.file_path = file_path

    def run(self):
        self.ai.add_content(self.file_path)
        self.result_ready.emit()
