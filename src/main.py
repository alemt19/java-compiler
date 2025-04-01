import sys
from pathlib import Path
from PyQt6.QtCore import QUrl, QObject, pyqtSlot
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel

from lexer import analizar, errores, crear_lexer, obtener_tokens
from parser import parse_code, get_errores_sint, crear_parser

lexer = crear_lexer()
parser = crear_parser(obtener_tokens())

class Bridge(QObject):
    def __init__(self, webview):
        super().__init__()
        self.webview = webview

    @pyqtSlot(str, result=str)
    def analisisLexicoJS(self, data):
        return analizar(data)
    
    @pyqtSlot(result=str)
    def analisisLexicoErroresJS(self):
        return errores()

    @pyqtSlot(str, result=str)
    def analisisSintacticoJS(self, data):
        return parse_code(parser, data, lexer)
    
    @pyqtSlot(result=str)
    def analisisSintacticoErroresJS(self):
        return get_errores_sint(parser)

    def enviarAJS(self, data):
        self.webview.page().runJavaScript(f"recibirDesdePython('{data}')")

app = QApplication(sys.argv)
view = QWebEngineView()

channel = QWebChannel()
bridge = Bridge(view)
channel.registerObject('pyObject', bridge)
view.page().setWebChannel(channel)

html_path = Path(__file__).parent / 'views' / 'index_v2.html'
view.load(QUrl.fromLocalFile(str(html_path.absolute())))

view.show()
sys.exit(app.exec())
