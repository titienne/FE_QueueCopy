import importlib
import os
import sys
import locale
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from tests.test_translation import _mock_pyqt

def setup_module(module):
    _mock_pyqt()

def reload_main():
    import main
    return importlib.reload(main)

def _module(monkeypatch):
    monkeypatch.setenv("APP_LANG", "en")
    return reload_main()

def test_language_detection(monkeypatch):
    monkeypatch.setenv("APP_LANG", "es")
    assert reload_main().LANG == "es"
    monkeypatch.setenv("APP_LANG", "auto")
    monkeypatch.setattr(locale, "getdefaultlocale", lambda: ("pt_BR", "UTF-8"))
    assert reload_main().LANG == "pt"
    monkeypatch.delenv("APP_LANG", raising=False)
    monkeypatch.setattr(locale, "getdefaultlocale", lambda: (None, None))
    assert reload_main().LANG == "en"

def test_save_load_tasks(tmp_path, monkeypatch):
    m = _module(monkeypatch)
    m.QUEUE_DIR = str(tmp_path); m.QUEUE_FILE = os.path.join(m.QUEUE_DIR, "tasks.json")
    tasks = [{"src": "a", "dst": "b"}]
    m.save_tasks(tasks)
    assert Path(m.QUEUE_FILE).exists()
    assert m.load_tasks() == tasks
    m.ensure_queue_file()

def test_copy_functions(tmp_path, monkeypatch):
    m = _module(monkeypatch)
    src_file = tmp_path / "f.txt"
    src_file.write_text("hello")
    src_dir = tmp_path / "src"
    src_dir.mkdir(); (src_dir / "f.txt").write_text("hello"); (src_dir / "g.txt").write_text("bye")
    dst_root = tmp_path / "dst"

    m.copy_file_with_resume(str(src_file), str(dst_root / "f.txt"))
    assert (dst_root / "f.txt").read_text() == "hello"

    m.copy_with_resume(str(src_dir), str(dst_root))
    assert (dst_root / "src" / "f.txt").read_text() == "hello"
    assert (dst_root / "src" / "g.txt").read_text() == "bye"

    dst = tmp_path / "out.txt"
    dst.write_text("he")
    m.copy_file_with_resume(str(src_file), str(dst))
    assert dst.read_text() == "hello"

def test_add_and_run_queue(tmp_path, monkeypatch):
    m = _module(monkeypatch)
    src = tmp_path / "a.txt"; src.write_text("x")
    tasks = m.run_queue(m.add_tasks([], [str(src)], str(tmp_path)), lambda *_: (_ for _ in ()).throw(Exception()))
    assert not tasks and (tmp_path / "a.txt").exists()
    tasks = m.run_queue([{"src": str(src), "dst": str(tmp_path)}], lambda *_: None); assert not tasks

def test_ensure_queue_file(tmp_path, monkeypatch):
    m = _module(monkeypatch)
    m.QUEUE_DIR = str(tmp_path)
    m.QUEUE_FILE = str(tmp_path / "tasks.json")
    m.ensure_queue_file()
    assert os.path.exists(m.QUEUE_FILE)
