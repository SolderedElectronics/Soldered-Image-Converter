# Create a class which will make a new PySide6 GUI object
# On this object, you can drag and drop images to be converted
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import QLabel
# This is a QLabel which has a 'droppable' area

class DropLabel(QLabel):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window  # Store the reference to the main window
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        # Collect all the file paths
        urls = event.mimeData().urls()
        file_paths = [url.toLocalFile() for url in urls]  # Collect all paths in a list

        # Now pass the list to a method in the main window for further processing
        self.main_window.handle_file_drop(file_paths)  # Pass the list
