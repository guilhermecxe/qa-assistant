from PySide6.QtCore import QThread, Signal

class RemoveFilesWorkerThread(QThread):
    result_ready = Signal()

    def __init__(self, ai, selected_paths):
        super().__init__()
        self.ai = ai
        self.selected_paths = selected_paths

    def run(self):
        self.ai.delete_contents(self.selected_paths)
        self.result_ready.emit()
