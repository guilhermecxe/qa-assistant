from PySide6.QtWidgets import QStatusBar
from PySide6.QtCore import QTimer

class StatusManager():
    FONT_COLOR = 'black'
    BACKGROUND_COLOR = {
        'success': '#e06b53',
        'warning': 'yellow',
        'error': '#3ec964',
    }

    def __init__(self, status:QStatusBar):
        self.status = status

    def clear(self):
        self.status.setStyleSheet('')
        self.status.clearMessage()

    def update(self, message_type, message, timeout=False):
        background_color = self.BACKGROUND_COLOR[message_type]
        font_color = self.FONT_COLOR
        self.status.setStyleSheet(
            'QStatusBar { background-color: ' + background_color + '; color: ' + font_color + ';}')
        self.status.showMessage(message)
        if timeout:
            QTimer.singleShot(timeout, self.clear)