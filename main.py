#!/usr/bin/env python3
from importlib import reload
from PyQt6.QtWidgets import QApplication

import translations as _t
import tasks as _tasks
from gui import QueueCopyGUI

reload(_t)

LANG = _t.LANG
tr = _t.tr
detect_lang = _t.detect_lang
QUEUE_DIR = _tasks.QUEUE_DIR
QUEUE_FILE = _tasks.QUEUE_FILE


def ensure_queue_file():
    _tasks.QUEUE_DIR = QUEUE_DIR
    _tasks.QUEUE_FILE = QUEUE_FILE
    _tasks.ensure_queue_file()


def load_tasks():
    _tasks.QUEUE_DIR = QUEUE_DIR
    _tasks.QUEUE_FILE = QUEUE_FILE
    return _tasks.load_tasks()


def save_tasks(tasks):
    _tasks.QUEUE_DIR = QUEUE_DIR
    _tasks.QUEUE_FILE = QUEUE_FILE
    _tasks.save_tasks(tasks)


def copy_file_with_resume(src, dst):
    _tasks.copy_file_with_resume(src, dst)


def copy_with_resume(src, dst_root):
    _tasks.copy_with_resume(src, dst_root)

add_tasks = _tasks.add_tasks
run_queue = _tasks.run_queue


__all__ = [
    "LANG",
    "tr",
    "detect_lang",
    "QUEUE_DIR",
    "QUEUE_FILE",
    "ensure_queue_file",
    "load_tasks",
    "save_tasks",
    "copy_file_with_resume",
    "copy_with_resume",
    "add_tasks",
    "run_queue",
    "QueueCopyGUI",
]


if __name__ == "__main__":
    app = QApplication([])
    window = QueueCopyGUI()
    window.show()
    app.exec()
