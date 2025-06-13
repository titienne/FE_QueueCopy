import os
import json
import shutil

QUEUE_DIR = os.path.expanduser("~/.queue_copy_gui")
QUEUE_FILE = os.path.join(QUEUE_DIR, "tasks.json")
CHUNK_SIZE = 1024 * 1024

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

def copy_file_with_resume(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    offset = os.path.getsize(dst) if os.path.exists(dst) else 0
    with open(src, "rb") as s, open(dst, "ab" if offset else "wb") as d:
        s.seek(offset)
        while True:
            buf = s.read(CHUNK_SIZE)
            if not buf:
                break
            d.write(buf)
    shutil.copystat(src, dst)

def copy_with_resume(src, dst_root):
    if os.path.isdir(src):
        base = os.path.basename(src.rstrip(os.sep))
        for root, _, files in os.walk(src):
            rel = os.path.relpath(root, src)
            target = os.path.join(dst_root, base, rel)
            os.makedirs(target, exist_ok=True)
            for f in files:
                copy_file_with_resume(os.path.join(root, f),
                                      os.path.join(target, f))
    else:
        copy_file_with_resume(src, os.path.join(dst_root, os.path.basename(src)))


def add_tasks(task_list, sources, dst):
    for src in sources:
        task_list.append({"src": src, "dst": dst})
    return task_list


def run_queue(tasks, on_error):
    done = []
    for t in list(tasks):
        try:
            copy_with_resume(t["src"], t["dst"])
            done.append(t)
        except Exception as exc:  # pragma: no cover - error path tested separately
            on_error(t, exc)
    return [t for t in tasks if t not in done]
