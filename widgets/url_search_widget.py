import os, sys
import urllib

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt5.QtCore import pyqtSignal

parentDir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
widget_class = uic.loadUiType(os.path.join(parentDir, "UI/url_search_widget.ui"))[0]

class UrlSearchWidget(QWidget, widget_class):

    click_url_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.url = None
        self.setupUi(self)
        self._loadUiInit()
        self._setEvent()

    def _loadUiInit(self):
        '''
        UI 초기화
        :return: None
        '''
        pass

    def _setEvent(self):
        self.btnUrl.clicked.connect(self._clickBtnUrl)
        pass

    def _clickBtnUrl(self):
        print(self.edtUrl.text())
        self.url = self.edtUrl.text()

        try:
            urllib.request.urlopen(self.url)
        except Exception as e:
            print("imageLoadUrl function  except HTTPError as e")
            QMessageBox.information(self,"Information:", "잘못된 접근입니다.(이미지가 아니거나 URL 오류)")
            self.edtUrl.setText("")
            return

        self.click_url_signal.emit()
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    url_search_widget = UrlSearchWidget()
    url_search_widget.show()
    exit(app.exec_())