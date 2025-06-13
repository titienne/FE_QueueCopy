#!/usr/bin/env python3
"""
queue_copy_gui.py

A PyQt6 application for drag-and-drop file/folder copy management with:
- Source area: drop files/folders, see count of items.
- Destination area: drop a single destination folder to enqueue all sources for copying there.
- Persistent queue: tasks stored in ~/.queue_copy_gui/tasks.json, surviving restarts and crashes.
- "Start Copy" button: processes the queue sequentially using a built-in Python copy routine with automatic resume of partial file copies.
"""
import sys
import os
import json
import shutil
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QListWidget, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt, QMimeData, QUrl

# Directory and file for task persistence
QUEUE_DIR = os.path.expanduser("~/.queue_copy_gui")
QUEUE_FILE = os.path.join(QUEUE_DIR, "tasks.json")

CHUNK_SIZE = 1024 * 1024  # 1MB chunks for file copying

def ensure_queue_file():
    os.makedirs(QUEUE_DIR, exist_ok=True)
    if not os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, "w") as f:
            json.dump([], f)


def load_tasks():
    ensure_queue_file()
    with open(QUEUE_FILE, "r") as f:
        return json.load(f)


def save_tasks(tasks):
    ensure_queue_file()
    with open(QUEUE_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def copy_file_with_resume(src_path, dst_path):
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    offset = 0
    if os.path.exists(dst_path):
        offset = os.path.getsize(dst_path)
    total_size = os.path.getsize(src_path)
    with open(src_path, 'rb') as sf, open(dst_path, 'ab' if offset else 'wb') as df:
        sf.seek(offset)
        while True:
            buf = sf.read(CHUNK_SIZE)
            if not buf:
                break
            df.write(buf)
    shutil.copystat(src_path, dst_path)


def copy_with_resume(src, dst_root):
    if os.path.isdir(src):
        base = os.path.basename(src.rstrip(os.sep))
        for root, dirs, files in os.walk(src):
            rel_path = os.path.relpath(root, src)
            target_dir = os.path.join(dst_root, base, rel_path)
            os.makedirs(target_dir, exist_ok=True)
            for name in files:
                sfile = os.path.join(root, name)
                dfile = os.path.join(target_dir, name)
                copy_file_with_resume(sfile, dfile)
    else:
        target = os.path.join(dst_root, os.path.basename(src))
        copy_file_with_resume(src, target)


class DropList(QListWidget):
    """A list widget that accepts file/folder drops."""
    def __init__(self, parent=None, only_dirs: bool=False):
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


class QueueCopyGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Queue Copy GUI")
        self.resize(600, 400)

        main_layout = QVBoxLayout(self)
        hl_layout = QHBoxLayout()

        # Source drop area
        self.src_list = DropList(self, only_dirs=False)
        self.src_label = QLabel("Dropped sources: 0")
        src_layout = QVBoxLayout()
        src_layout.addWidget(QLabel("Source Area: drag files/folders here"))
        src_layout.addWidget(self.src_list)
        src_layout.addWidget(self.src_label)
        hl_layout.addLayout(src_layout)

        # Destination drop area
        self.dst_list = DropList(self, only_dirs=True)
        self.dst_label = QLabel("No destination folder")
        dst_layout = QVBoxLayout()
        dst_layout.addWidget(QLabel("Destination Area: drag a folder here"))
        dst_layout.addWidget(self.dst_list)
        dst_layout.addWidget(self.dst_label)
        hl_layout.addLayout(dst_layout)

        main_layout.addLayout(hl_layout)

        # Persistent queue display
        self.queue_widget = QListWidget()
        main_layout.addWidget(QLabel("Persistent copy queue:"))
        main_layout.addWidget(self.queue_widget)

        # Control buttons
        btn_layout = QHBoxLayout()
        self.run_btn = QPushButton("Start Copy")
        self.run_btn.clicked.connect(self.run_copy)
        btn_layout.addWidget(self.run_btn)
        main_layout.addLayout(btn_layout)

        # Load existing tasks
        self.tasks = load_tasks()
        self.refresh_queue()

        # Auto-enqueue upon destination drop
        self.dst_list.itemDoubleClicked.connect(self.enqueue_tasks)

    def update_counts(self):
        count = self.src_list.count()
        self.src_label.setText(f"Dropped sources: {count}")
        if self.dst_list.count() > 0 and count > 0:
            self.enqueue_tasks()

    def enqueue_tasks(self):
        dst = self.dst_list.item(self.dst_list.count() - 1).text()
        for i in range(self.src_list.count()):
            src = self.src_list.item(i).text()
            self.tasks.append({'src': src, 'dst': dst})
        save_tasks(self.tasks)
        self.refresh_queue()
        self.src_list.clear()
        self.dst_list.clear()
        self.src_label.setText("Dropped sources: 0")
        self.dst_label.setText("No destination folder")

    def refresh_queue(self):
        self.queue_widget.clear()
        for t in self.tasks:
            self.queue_widget.addItem(f"{t['src']} → {t['dst']}")

    def run_copy(self):
        completed = []
        for t in list(self.tasks):
            src, dst = t['src'], t['dst']
            self.queue_widget.addItem(f"Processing: {src} → {dst}")
            QApplication.processEvents()
            try:
                copy_with_resume(src, dst)
                completed.append(t)
            except Exception as e:
                QMessageBox.warning(self, "Copy Error", f"Failed to copy {src}: {e}")
        self.tasks = [t for t in self.tasks if t not in completed]
        save_tasks(self.tasks)
        self.refresh_queue()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QueueCopyGUI()
    window.show()
    sys.exit(app.exec())
