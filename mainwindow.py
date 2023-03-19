# This Python file uses the following encoding: utf-8
import sys
from PyQt6 import uic, QtWidgets, QtGui, QtCore
from objeto import Tipo
import images_rcc
from dialog import Dialog
from windowtransformation import WindowTransformation


class MainWindow(QtWidgets.QMainWindow):
    """
    Janela principal do qt que possui os widgets
    """
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setup_view()
        self.transform = WindowTransformation()

        # self.listOfCurrentObjects.setObjectName("listView")
        # self.listOfCurrentObjects.addItems(["One", "two"])
        # self.comboBoxOfTypes.addItems([Tipo.POLIGONO.value, Tipo.SEGMENTO_RETA.value, Tipo.PONTO.value])

        self.addObjectButton.clicked.connect(self.show_dialog)
        self.zoomInButton.clicked.connect(self.zoom_in)

    def setup_view(self):
        uic.loadUi("UI/MainWindow.ui", self) #carrega o arquivo de interface gráfica para a janela do qt
        self.setWindowTitle("Sistema básico interativo - Computação gráfica")

        self.container = self.labelContainerForCanvas
        canvas = QtGui.QPixmap(531, 511)
        canvas.fill(QtCore.Qt.GlobalColor.white)
        self.container.setPixmap(canvas)

    def show_dialog(self):
        dialog = Dialog()
        dialog.show()
        dialog.exec()

    def draw_line(self, x1: int, y1: int, x2: int, y2: int):
        canvas = self.container.pixmap()
        painter = QtGui.QPainter(canvas)
        painter.drawLine(x1, y1, x2, y2)
        painter.end()
        self.container.setPixmap(canvas)

    def draw_point(self, x, y):
        canvas = self.container.pixmap()
        painter = QtGui.QPainter(canvas)
        painter.drawPoint(x, y)
        painter.end()
        self.container.setPixmap(canvas)

    def zoom_in(self):
        pass #implementar


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    window = MainWindow()    
    window.show()
    sys.exit(app.exec())
