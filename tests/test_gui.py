import os
import sys
import types
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from tests.test_translation import _mock_pyqt

def setup_module(module):
    _mock_pyqt()


def _event(paths):
    urls = [types.SimpleNamespace(toLocalFile=lambda p=str(p): p) for p in paths]
    mime = types.SimpleNamespace(hasUrls=lambda: True, urls=lambda: urls)
    return types.SimpleNamespace(
        mimeData=lambda: mime,
        acceptProposedAction=lambda: None,
        ignore=lambda: None,
    )

def _event_empty():
    mime = types.SimpleNamespace(hasUrls=lambda: False, urls=lambda: [])
    return types.SimpleNamespace(
        mimeData=lambda: mime,
        acceptProposedAction=lambda: None,
        ignore=lambda: None,
    )


def test_drop_list(tmp_path):
    import droplist

    parent = types.SimpleNamespace(update_counts=lambda: None)
    dl = droplist.DropList(parent, True)
    folder = tmp_path / "dir"
    folder.mkdir()
    other = tmp_path / "f"
    other.write_text("x")

    event = _event([folder, other])
    dl.dragEnterEvent(event)
    dl.dropEvent(event)
    dl.dragEnterEvent(_event_empty())

    assert dl.count() == 1
    assert dl.item(0).text() == str(folder)


def test_queue_copy_gui(monkeypatch, tmp_path):
    import gui

    monkeypatch.setattr(gui, "load_tasks", lambda: [])
    monkeypatch.setattr(gui, "save_tasks", lambda tasks: None)

    error = [False]

    def rq(tasks, cb):
        if not error[0]:
            error[0] = True
            cb(tasks[0], Exception("x"))
            return tasks
        return []

    monkeypatch.setattr(gui, "run_queue", rq)
    g = gui.QueueCopyGUI()

    g.src_l.addItem("a")
    g.dst_l.addItem(str(tmp_path))
    g.enqueue()
    assert g.tasks

    g.run_copy()
    assert g.tasks

    error[0] = True
    g.run_copy()
    assert not g.tasks

    g.set_lang("fr")
    g.set_lang("auto")
