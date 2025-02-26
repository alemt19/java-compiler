import sys
from os import path
from pathlib import Path
from PyQt6.QtCore import QUrl, QObject, pyqtSlot
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel

sys.path.insert(0, path.join(".", "lexer"))
from lexer import analizar

class Bridge(QObject):
    def __init__(self, webview):
        super().__init__()
        self.webview = webview

    @pyqtSlot(str, result=str)
    def analisisLexicoJS(self, data):
        return analizar(data)

    def enviarAJS(self, data):
        self.webview.page().runJavaScript(f"recibirDesdePython('{data}')")

app = QApplication(sys.argv)
view = QWebEngineView()

channel = QWebChannel()
bridge = Bridge(view)
channel.registerObject('pyObject', bridge)
view.page().setWebChannel(channel)

html_path = Path(__file__).parent / 'views' / 'index_optimizado.html'
view.load(QUrl.fromLocalFile(str(html_path.absolute())))

view.show()
sys.exit(app.exec())
