from PyQt6.QtWidgets import QListWidget
import os

class DropList(QListWidget):
    def __init__(self, parent=None, only_dirs=False):
        super().__init__(parent)
        self.only_dirs = only_dirs
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if self.only_dirs and not os.path.isdir(path):
                continue
            self.addItem(path)
        self.parent().update_counts()
