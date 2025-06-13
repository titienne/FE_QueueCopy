import importlib, os, sys, types
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
def _mock_pyqt():
    class B:
        def __init__(self,*a,**k):pass
        def addWidget(self,*a):pass
        def addLayout(self,*a):pass
        def addMenu(self,*a):return self
        def addAction(self,*a,**k):pass
        def setText(self,*a):pass
        def setToolTip(self,*a):pass
        def setWindowTitle(self,*a):pass
        def resize(self,*a):pass
        def setAcceptDrops(self,*a):pass
        def show(self,*a):pass
        def exec(self,*a):pass
    class Sig:
        def connect(self,f):self.f=f
    class QListWidget(B):
        def __init__(self,parent=None,*a,**k):self._p=parent;self._it=[];self.itemDoubleClicked=Sig()
        def addItem(self,t):self._it.append(t)
        def clear(self):self._it.clear()
        def count(self):return len(self._it)
        def item(self,i):return types.SimpleNamespace(text=lambda:self._it[i])
        def parent(self):return self._p
    class QPushButton(B):
        def __init__(self,*a,**k):self.clicked=Sig()
    class QLabel(B):pass
    class Layout(B):pass
    class QMenuBar(B):pass
    class QMessageBox:
        @staticmethod
        def warning(*a,**k):pass
    class QUrl:
        def __init__(self,p):self._p=p
        def toLocalFile(self):return self._p
    qt=types.ModuleType('PyQt6');w=types.ModuleType('PyQt6.QtWidgets');c=types.ModuleType('PyQt6.QtCore')
    w.QApplication=B;w.QWidget=B;w.QVBoxLayout=Layout;w.QHBoxLayout=Layout
    w.QLabel=QLabel;w.QListWidget=QListWidget;w.QPushButton=QPushButton
    w.QMessageBox=QMessageBox;w.QMenuBar=QMenuBar
    c.QMimeData=B;c.QUrl=QUrl
    qt.QtWidgets=w;qt.QtCore=c
    sys.modules['PyQt6']=qt;sys.modules['PyQt6.QtWidgets']=w;sys.modules['PyQt6.QtCore']=c

_mock_pyqt()
import main

def test_translations():
    mapping={'fr':'Démarrer la copie','es':'Iniciar copia','pt':'Iniciar cópia','de':'Kopie starten','nl':'Kopie starten'}
    for lang,text in mapping.items():
        os.environ['APP_LANG']=lang
        importlib.reload(main)
        assert main.tr('Start Copy')==text
    os.environ['APP_LANG']='en'
    importlib.reload(main)
    assert main.tr('Start Copy')=='Start Copy'
def test_run_main(monkeypatch):
    import runpy
    monkeypatch.setattr('main.QueueCopyGUI', lambda: types.SimpleNamespace(show=lambda:None))
    runpy.run_module('main', run_name='__main__')
