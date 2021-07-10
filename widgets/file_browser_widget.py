import sys, os, shutil
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QFileSystemModel, QInputDialog, QLineEdit, QApplication
from PyQt5.QtCore import pyqtSignal
from config import get_default_path

parentDir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
widget_class = uic.loadUiType(os.path.join(parentDir, "UI/file_browser_widget.ui"))[0]

class FileBrowserWidget(QWidget, widget_class):

    click_file_signal = pyqtSignal()
    double_click_file_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.root_path = get_default_path()
        #print(">>>>>>>>>>>>>>>>>>>>"+self.path)
        self.index = None
        self.file_path = None
        self.model = QFileSystemModel()

        self.setupUi(self)
        self._loadUiInit()
        self._setEvent()

        print('RootPath : {}'.format(self.root_path))  #

    def _loadUiInit(self):
        '''
        UI 초기화
        :return: None
        '''
        self.fileTreeView.setModel(self.model)
        self.fileTreeView.setColumnWidth(0,400)
        self.model.setNameFilters(["*.jpg","*.jpeg", "*.png", "*.bmp", "*.gif"])
        self.model.setNameFilterDisables(False)
        self.model.setRootPath(self.root_path)
        self.fileTreeView.setRootIndex(self.model.index(self.root_path))

        self.fileTreeView.hideColumn(2)
        self.fileTreeView.hideColumn(3)
        pass

    def _setEvent(self):
        self.fileTreeView.clicked.connect(self._clickedFile)
        self.fileTreeView.doubleClicked.connect(self._doubleClickedFile)
        self.btnDel.clicked.connect(self._del)
        self.btnRen.clicked.connect(self._ren)
        self.btnFilter.clicked.connect(self._btnFilter)
        self.edtFilter.returnPressed.connect(self._btnFilter)

    def _clickedFile(self, index):
        print("_clickedFile start")
        self.index = index
        self.file_path = self.model.filePath(index)
        print(self.file_path)
        self.click_file_signal.emit()
        print("_clickedFile end")
        pass

    def _doubleClickedFile(self, index):
        print("_doubleClickedFile start")
        self.file_path = self.model.filePath(index)
        print(self.file_path)
        self.double_click_file_signal.emit()
        print("_doubleClickedFile end")
        pass

    def _btnFilter(self):
        fn = self.edtFilter.text()
        print(fn)
        self.model.setNameFilters([fn+"*.jpg", fn+"*.jpeg", fn+"*.png", fn+"*.bmp", fn+"*.gif"])

    def getFilePath(self):
        return self.file_path

    def _del(self):
        os.chdir(self.model.filePath(self.model.parent(self.index)))
        fname = self.model.fileName(self.index)


        try:
            if not self.model.isDir(self.index):
                os.unlink(fname)
                print(fname + '파일 삭제')
            else:
                shutil.rmtree(fname)
                print(fname + '폴더 삭제')
        except:
            print('에러발생')

    def _ren(self):
        os.chdir(self.model.filePath(self.model.parent(self.index)))
        fname = self.model.fileName(self.index)
        text, res = QInputDialog.getText(self,"이름변경", "바꿀이름을 입력하세요",
                                         QLineEdit.Normal, fname)

        if res:
            while True:
                self.ok = True
                for i in os.listdir(os.getcwd()):
                    print(i)
                    if i == text:
                        text, res = QInputDialog.getText(self,"중복 오류!", "바꿀 이름을 입력하세요",
                                                         QLineEdit.Normal, text)
                        if not res:
                            return
                        self.ok = False
                if self.ok:
                    break
            os.rename(fname,text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    file_browser_widget = FileBrowserWidget()
    file_browser_widget.show()
    exit(app.exec_())