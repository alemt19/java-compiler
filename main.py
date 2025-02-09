import sys
from pathlib import Path
from PyQt6.QtCore import QUrl, QObject, pyqtSlot
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel

class Bridge(QObject):
    @pyqtSlot()
    def metodoPython(self):
        print("JavaScript llamó a Python!")

app = QApplication(sys.argv)
view = QWebEngineView()

# Configurar canal de comunicación
channel = QWebChannel()
bridge = Bridge()
channel.registerObject('pyObject', bridge)
view.page().setWebChannel(channel)

# Cargar archivo HTML
html_path = Path(__file__).parent / 'views' / 'index.html'
view.load(QUrl.fromLocalFile(str(html_path.absolute())))

view.show()
sys.exit(app.exec())
