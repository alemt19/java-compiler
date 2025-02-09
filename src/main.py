# main.py
import sys
from pathlib import Path
from PyQt6.QtCore import QUrl, QObject, pyqtSlot, QTimer
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel

class Bridge(QObject):
    def __init__(self, webview):
        super().__init__()
        self.webview = webview

    @pyqtSlot(str, result=str)
    def metodoPython(self, data):
        print(f"Dato recibido desde JS: {data}")
        # Enviamos respuesta a JS después de 1 segundo
        QTimer.singleShot(1000, lambda: self.enviarAJS("Python dice: ¡Hola de vuelta!"))
        return "Python recibió: " + data

    def enviarAJS(self, mensaje):
        self.webview.page().runJavaScript(f"recibirDesdePython('{mensaje}')")

app = QApplication(sys.argv)
view = QWebEngineView()

channel = QWebChannel()
bridge = Bridge(view)
channel.registerObject('pyObject', bridge)
view.page().setWebChannel(channel)

html_path = Path(__file__).parent / 'views' / 'index.html'
view.load(QUrl.fromLocalFile(str(html_path.absolute())))

view.show()
sys.exit(app.exec())
