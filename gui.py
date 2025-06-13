from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QListWidget, QPushButton, QMessageBox, QMenuBar
)
from translations import tr, detect_lang, LANG
from tasks import load_tasks, save_tasks, add_tasks, run_queue
from droplist import DropList

class QueueCopyGUI(QWidget):
    def __init__(self):
        super().__init__(); self.setWindowTitle(tr("Queue Copy GUI")); self.resize(600,400)
        v=QVBoxLayout(self); m=QMenuBar(); v.addWidget(m)
        l=m.addMenu(tr("Language")); l.addAction(tr("Auto"),lambda:self.set_lang("auto"))
        for c,t in [("en","English"),("fr","Français")]: l.addAction(t,lambda _,x=c:self.set_lang(x))
        a=QHBoxLayout(); v.addLayout(a)
        self.src_t,self.src_l,self.src_lbl=self._area(a); self.dst_t,self.dst_l,self.dst_lbl=self._area(a,True)
        self.queue=QListWidget(); v.addWidget(self.queue)
        self.run_btn=QPushButton(); self.run_btn.clicked.connect(self.run_copy)
        b=QHBoxLayout(); b.addWidget(self.run_btn); v.addLayout(b)
        self.tasks=load_tasks(); self.refresh(); self.dst_l.itemDoubleClicked.connect(self.enqueue); self.update_texts()

    def _area(self, parent, dirs=False):
        box=QVBoxLayout(); t=QLabel(); view=DropList(self,dirs); lbl=QLabel()
        for w in (t,view,lbl): box.addWidget(w)
        parent.addLayout(box); return t,view,lbl

    def update_counts(self):
        n=self.src_l.count(); self.src_lbl.setText(tr("Dropped sources: {count}").format(count=n))
        if self.dst_l.count() and n: self.enqueue()

    def enqueue(self):
        dst=self.dst_l.item(self.dst_l.count()-1).text(); srcs=[self.src_l.item(i).text() for i in range(self.src_l.count())]
        add_tasks(self.tasks,srcs,dst); save_tasks(self.tasks); self.refresh(); self.src_l.clear(); self.dst_l.clear(); self.update_counts();
        self.dst_lbl.setText(tr("No destination folder"))

    def refresh(self):
        self.queue.clear(); [self.queue.addItem(f"{t['src']} → {t['dst']}") for t in self.tasks]

    def set_lang(self, code):
        global LANG; LANG=detect_lang() if code=="auto" else code; self.update_texts()

    def update_texts(self):
        self.setWindowTitle(tr("Queue Copy GUI")); self.src_t.setText(tr("Source Area: drag files/folders here"))
        self.dst_t.setText(tr("Destination Area: drag a folder here")); self.queue.setToolTip(tr("Persistent copy queue:"))
        self.run_btn.setText(tr("Start Copy"));
        if not self.dst_l.count(): self.dst_lbl.setText(tr("No destination folder")); self.update_counts()

    def run_copy(self):
        def err(t,e): QMessageBox.warning(self,tr("Copy Error"),tr("Failed to copy {src}: {e}").format(src=t['src'],e=e))
        self.tasks=run_queue(self.tasks,err); save_tasks(self.tasks); self.refresh()
