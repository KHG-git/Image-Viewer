import sys

from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtPrintSupport import QPrintDialog
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu, QMessageBox, qApp
from PyQt5.QtCore import Qt

from config import get_config
from libs.version import __version__
from widgets.canvas_widget import CanvasWidget
from widgets.file_browser_widget import FileBrowserWidget
from widgets.url_search_widget import UrlSearchWidget

__appname__ = 'Image Viewer'
form_class = uic.loadUiType("UI/image_viewer_main.ui")[0]

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.file_browser_widget = FileBrowserWidget()
        self.canvas_widget = CanvasWidget()
        self.url_search_widget = UrlSearchWidget()

        self.setupUi(self)
        self.createActions()
        self.createMenus()

        self._initData()
        self._setEvent()
        self._loadUiInit()

    def _initData(self):
        '''
        Data 초기화
        :return:
        '''
        self._config = get_config()

        pass

    def _loadUiInit(self):
        '''
        UI 초기화
        :return: None
        '''
        self.setWindowTitle("{title} ({version})".format(title=__appname__, version=__version__))
        self.splitter.setSizes([200, 400])
        self.layout_canvas.addWidget(self.canvas_widget)
        self.file_browser_area.addWidget(self.file_browser_widget)
        self.url_search_area.addWidget(self.url_search_widget)
        self.statusbar.showMessage("")
        self.url_search_widget.edtUrl.setText("")

        self.updateActions(0)

        #self.setWindowIcon(QIcon('UI/images/icon/appicon.png'))
        pass

    def _setEvent(self):
        #file tree view에서 파일 선택시 연결
        #self.file_browser_widget.click_file_signal.connect(self._chageStatusBar)
        self.file_browser_widget.double_click_file_signal.connect(self._openFile)
        self.url_search_widget.click_url_signal.connect(self._openFileUrl)
        self.canvas_widget.clear_signal.connect(self._loadUiInit)
        self.canvas_widget.update_action_signal.connect(lambda: self.updateActions(1))
        self.canvas_widget.update_action_signal.connect(self._chageStatusBar)
        pass

    def _chageStatusBar(self):
        print("_chageStatusBar start")
        self.msg = self.canvas_widget.image_path
        self.file_width = self.canvas_widget.image_width
        self.file_height = self.canvas_widget.image_height

        if self.file_width is not None:
            self.msg += " (" +  str(self.file_width) + "," + str(self.file_height) + ")"
        else:
            pass

        self.statusbar.showMessage(self.msg)

        print("_chageStatusBar end")
        pass

    def _openFile(self):
        print("double_click_file_signal : openFile  start   : main.py    ")
        self.file_path = self.file_browser_widget.getFilePath()
        print("_openFile>file_path : "+ self.file_path)
        self.canvas_widget.imageLoad(self.file_path)
        print("double_click_file_signal : openFile  end   : main.py    ")
        pass

    def _openFileUrl(self):
        self.url = self.url_search_widget.url
        self.canvas_widget.imageLoadUrl(self.url)
        pass

    def createActions(self):
        self.openAct = QAction("&Open...", self, shortcut="Ctrl+O", triggered=self.canvas_widget.openFile)
        self.printAct = QAction("&Print...", self, shortcut="Ctrl+P", enabled=False, triggered=self.print_)
        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
        self.zoomInAct = (QAction("Zoom &In (25%)", self, shortcut="Ctrl++", enabled=False, triggered=self.canvas_widget.zoomIn))
        self.zoomOutAct = QAction("Zoom &Out (25%)", self, shortcut="Ctrl+-", enabled=False, triggered=self.canvas_widget.zoomOut)
        self.normalSizeAct = QAction("&Normal Size", self, shortcut="Ctrl+S", enabled=False, triggered=self.canvas_widget.normalSize)
        self.fitToWindowAct = QAction("&Fit to Window", self, enabled=False, checkable=False, shortcut="Ctrl+F", triggered=self.canvas_widget.fitToWindow)
        self.aboutAct = QAction("&About", self, triggered=self.about)
        self.aboutQtAct = QAction("About &Qt", self, triggered=qApp.aboutQt)

    def createMenus(self):
        #self.fileMenu = QMenu("&File", self)
        self.menufile.addAction(self.openAct)
        self.menufile.addAction(self.printAct)
        self.menufile.addSeparator()
        self.menufile.addAction(self.exitAct)

        #self.viewMenu = QMenu("&View", self)
        self.menuView.addAction(self.zoomInAct)
        self.menuView.addAction(self.zoomOutAct)
        self.menuView.addAction(self.normalSizeAct)
        self.menuView.addSeparator()
        self.menuView.addAction(self.fitToWindowAct)

        #self.helpMenu = QMenu("&Help", self)
        self.menuHelp.addAction(self.aboutAct)
        self.menuHelp.addAction(self.aboutQtAct)

        #self.menuBar().addMenu(self.fileMenu)
        #self.menuBar().addMenu(self.viewMenu)
        #self.menuBar().addMenu(self.helpMenu)


    def updateActions(self, tf):
        print("updateActions")
        if( tf == 1):
            self.zoomInAct.setEnabled(True)
            self.zoomOutAct.setEnabled(True)
            self.normalSizeAct.setEnabled(True)
            self.fitToWindowAct.setEnabled(True)
        else:
            self.zoomInAct.setEnabled(False)
            self.zoomOutAct.setEnabled(False)
            self.normalSizeAct.setEnabled(False)
            self.fitToWindowAct.setEnabled(False)


    def about(self):
        QMessageBox.about(self, "About Image Viewer",
                          "<p>The <b>Image Viewer</b> example shows how to combine "
                          "QLabel and QScrollArea to display an image. QLabel is "
                          "typically used for displaying text, but it can also display "
                          "an image. QScrollArea provides a scrolling view around "
                          "another widget. If the child widget exceeds the size of the "
                          "frame, QScrollArea automatically provides scroll bars.</p>"
                          "<p>The example demonstrates how QLabel's ability to scale "
                          "its contents (QLabel.scaledContents), and QScrollArea's "
                          "ability to automatically resize its contents "
                          "(QScrollArea.widgetResizable), can be used to implement "
                          "zooming and scaling features.</p>"
                          "<p>In addition the example shows how to use QPainter to "
                          "print an image.</p>")

    def print_(self):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            size = self.imageLabel.pixmap().size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.imageLabel.pixmap().rect())
            painter.drawPixmap(0, 0, self.imageLabel.pixmap())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    exit(app.exec_())