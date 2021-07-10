import os, sys, shutil
import urllib.request
from urllib.error import HTTPError

from PyQt5 import uic, QtCore
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QAction, QMainWindow, QMenu, \
                            QSizePolicy, QMessageBox, QFileDialog, \
                            QApplication, QScrollArea, QLabel, qApp
from datetime import datetime
from PyQt5.QtGui import *
from config import get_default_path
import platform
#from Foundation import NSURL

# Use NSURL as a workaround to pyside/Qt4 behaviour for dragging and dropping on OSx
op_sys = platform.system()

parentDir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
widget_class = uic.loadUiType(os.path.join(parentDir, "UI/canvas_widget.ui"))[0]

class CanvasWidget(QWidget,  widget_class):

    clear_signal = pyqtSignal()
    update_action_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()
        #self.window = parent
        self.image = None
        self.image_path = None
        self.scaleFactor = 1.0
        self.image_size = None
        self.image_width = None
        self.image_height = None
        self.root_path = get_default_path()
        self.url_image = "url_image_"
        self.url_ext = ".jpg"
        self.now = None
        self.setupUi(self)
        self.spin_value_default = self.spin.value()
        self._loadUiInit()
        self._setEvent()

    def _loadUiInit(self):
        '''
        UI 초기화
        :return: None
        '''

        print("_loadUiInit")

        self.clearLayout(self.layoutCanvas)

        self.image = None
        self.image_path = None
        self.scaleFactor = 1.0
        self.image_width = None
        self.image_height = None

        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)
        self.imageLabel.accessDrops = True

        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setVisible(False)

        self.layoutCanvas.addWidget(self.scrollArea)

        self.initSpin()

        self.clear_signal.emit()

        pass

    def _setEvent(self):
        self.spin.valueChanged.connect(self.slider.setValue)
        self.slider.valueChanged.connect(self.spin.setValue)
        self.btnFileOpen.clicked.connect(self.openFile)
        self.btnInit.clicked.connect(self._loadUiInit)

        self.scrollArea.mouseMoveEvent = self.mouseMoveEventLeft
        self.scrollArea.mousePressEvent = self.mousePressEventLeft
        self.scrollArea.mouseReleaseEvent = self.mouseReleaseEventLeft

        self.btnZoomIn.clicked.connect(self.zoomIn)
        self.btnZoomOut.clicked.connect(self.zoomOut)
        self.btnZoomActual.clicked.connect(self.normalSize)
        self.btnZoomExtents.clicked.connect(self.fitToWindow)

        #spin과 slider은 같은 이벤트를 사용
        self.spin.valueChanged.connect(self.spinValueChanged)
        #self.slider.valueChanged.connect(self.spinValueChanged)


    def openFile(self):
        options = QFileDialog.Options()
        fileName = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                               'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
        print("filename : {}".format(fileName[0]))

        if fileName[0]:
            self.image = QImage(fileName[0])
            self.image_path = fileName[0]  # 파일 경로 저장
            if self.image.isNull():
                QMessageBox.information(self, "Image Viewer", "Cannot load %s." % fileName)
                return

            self.imageLoad(self.image_path)

    def imageLoad(self, fname):
        self.clear_signal.emit()
        try:
            self.image_path = fname
            print("_imageLoad function start")
            self.scrollArea.setWidgetResizable(False)
            print(self.image_path)

            self.image = QImage(fname)
            self.image_size = QPixmap.fromImage(self.image).size()
            self.image_width = self.image_size.width()
            self.image_height = self.image_size.height()
            self.imageLabel.setGeometry(0,0,self.image_width, self.image_height)

            self.imageLabel.setPixmap(QPixmap.fromImage(self.image))
            self.imageLabel.adjustSize()
            self.scrollArea.setVisible(True)

            self.initSpin()
            #parent의 함수를 access 못하는 관계로 signal로 처리 함
            self.update_action_signal.emit()

        except Exception as e:
            QMessageBox.information("잘못된 접근입니다.(이미지가 아니거나 URL 오류)")

        print("_imageLoad function end")

        pass

    def imageLoadUrl(self, url):
        print("imageLoadUrl function start(try)")
        self.now = datetime.now()  # 현재 시간 가져오기

        #url 이미지 파일명 생성
        self.image_path = self.root_path + self.url_image + self.now.strftime("%Y%m%d%H%M%S") + self.url_ext
        print(self.image_path)
        try:
            urllib.request.urlretrieve(url, self.image_path)
        except Exception as e:
            print("imageLoadUrl function  except HTTPError as e")
            QMessageBox.information(self,"Information:", "잘못된 접근입니다.(이미지가 아니거나 URL 오류)")
            self.clear_signal.emit()
            return

        print("imageLoadUrl function start(open)")
        self.imageLoad(self.image_path)

        print("imageLoadUrl function end")

        pass


    #사용 안함.
    def _initToolBar(self):
        self.zoom_in = QAction(QIcon('UI/images/icon/zoom_in.png'), 'zoom_in', self)
        self.zoom_in.setStatusTip('zoom in')
        #self.zoom_in.setSeparator(False)
        self.toolbar = self.addToolBar('zoom_in')
        self.toolbar.addAction(self.zoom_in)

        self.zoom_out = QAction(QIcon('UI/images/icon/zoom_out.png'), 'zoom_out', self)
        #self.zoom_out.setStatusTip('zoom out')
        self.toolbar = self.addToolBar('zoom_out')
        self.toolbar.addAction(self.zoom_out)

        self.zoom_to_actual = QAction(QIcon('UI/images/icon/zoom_to_actual_size.png'), 'zoom_to_actual', self)
        self.zoom_to_actual.setStatusTip('zoom actual')
        self.toolbar = self.addToolBar('zoom_to_actual')
        self.toolbar.addAction(self.zoom_to_actual)

        self.zoom_to_extents = QAction(QIcon('UI/images/icon/zoom_to_extents.png'), 'zoom_to_extents', self)
        self.zoom_to_extents.setStatusTip('zoom extents')
        self.toolbar = self.addToolBar('zoom_to_extents')
        self.toolbar.addAction(self.zoom_to_extents)

    # The following three methods set up dragging and dropping for the app
    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls: e.accept()
        else: e.ignore()

    def dragMoveEvent(self, e):
        if e.mimeData().hasUrls: e.accept()
        else: e.ignore()

    def dropEvent(self, e):
        """ 
        Drop files directly onto the widget File locations are stored in
        fname :param e: :return:
        """
        if e.mimeData().hasUrls:
            e.setDropAction(QtCore.Qt.CopyAction)
            e.accept()
            # Workaround for OSx dragging and dropping
            for url in e.mimeData().urls():
                #if op_sys == 'Darwin':
                #    fname = str(NSURL.URLWithString_(str(url.toString())).filePathURL().path())
                #else:
                fname = str(url.toLocalFile())

            if os.path.dirname(fname) != self.root_path:
                shutil.copy(fname, self.root_path)
            else:
                pass

            self.imageLoad(fname)

        else:
            e.ignore()


    def mousePressEventLeft(self, event):
        self.pressed = True
        self.imageLabel.setCursor(Qt.ClosedHandCursor)
        self.initialPosX = self.scrollArea.horizontalScrollBar().value() + event.pos().x()
        self.initialPosY = self.scrollArea.verticalScrollBar().value() + event.pos().y()

    def mouseReleaseEventLeft(self, event):
        self.pressed = False
        self.imageLabel.setCursor(Qt.OpenHandCursor)
        self.initialPosX = self.scrollArea.horizontalScrollBar().value()
        self.initialPosY = self.scrollArea.verticalScrollBar().value()

    def mouseMoveEventLeft(self, event):
        if self.pressed:
            self.scrollArea.horizontalScrollBar().setValue(self.initialPosX - event.pos().x())
            self.scrollArea.verticalScrollBar().setValue(self.initialPosY - event.pos().y())
            pass

    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        #self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        #self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

    def fitToWindow(self):
        #fitToWindow = self.fitToWindowAct.isChecked()
        #self.scrollArea.setWidgetResizable(fitToWindow)
        #if not fitToWindow:
        #    self.normalSize()
        #    print("if not fitToWindow")
        #self.imageLabel.setScaledContents(True)
        self.scrollArea.setWidgetResizable(True)
        self.initSpin()

    def zoomIn(self, value):
        self.scrollArea.setWidgetResizable(False)
        if not value or value == 0:
            self.scaleImage(1.25)
        else:
            self.scaleImage(value)

    def zoomOut(self, value):
        self.scrollArea.setWidgetResizable(False)
        if not value or value == 0:
            self.scaleImage(0.8)
        else:
            self.scaleImage(value)

    def normalSize(self):
        self.scrollArea.setWidgetResizable(False)
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0
        self.initSpin()

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))

    def initSpin(self):
        self.spin.setValue(self.spin_value_default)
        self.spin_value_curr = self.spin_value_default
        self.spin_value_prev = self.spin_value_default

    def spinValueChanged(self):
        if self.imageLabel.pixmap() != None:
            self.spin_value_prev = self.spin_value_curr
            self.spin_value_curr = self.spin.value()
            value = self.spin_value_curr - self.spin_value_prev
            if value > 0:
                self.scaleImage(1.01)
            else:
                self.scaleImage(0.99)
        else:
            return
        pass

    def clearLayout(self, layout):
        layout =self.layoutCanvas
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    canvas_widget = CanvasWidget()
    canvas_widget.show()
    exit(app.exec_())