from PySide6.QtCore import QObject, Qt

class ClickableLabelEventFilter(QObject):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def eventFilter(self, watched, event):
        if event.type() == event.MouseButtonPress and event.button() == Qt.LeftButton:
            self.callback()
            return True
        return super().eventFilter(watched, event)