import sys
from pathlib import Path
from PyQt6.QtCore import QUrl, QObject, pyqtSlot
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel

from lexer import analizar, errores, crear_lexer, obtener_tokens
from parser import parse_code, get_errores_sint, crear_parser, get_ast_str, CodeGeneratorVisitor

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
        ast = parse_code(parser, data, lexer)
        return get_ast_str(ast)
    
    @pyqtSlot(result=str)
    def analisisSintacticoErroresJS(self):
        return get_errores_sint(parser)

    @pyqtSlot(str, result=str)
    def generarCodigoJS(self, data):
        ast = parse_code(parser, data, lexer)
        if ast:
            # Crea el visitor y genera el código Python
            visitor = CodeGeneratorVisitor()
            python_code = ast.accept(visitor)

            # Imprime o guarda el código Python generado
            return python_code
        else:
            return "Error al parsear el código Java."


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
