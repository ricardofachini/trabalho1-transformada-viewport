# This Python file uses the following encoding: utf-8
import sys
from PyQt6 import uic, QtWidgets, QtGui, QtCore

import images_rcc

from dialog import Dialog
from objeto import Tipo

from windowtransformation import WindowTransformation
from displayfile import DisplayFile

from Ponto import Ponto
from Reta import Reta
from Poligono import WireFrame



class MainWindow(QtWidgets.QMainWindow):
    """
    Janela principal do qt que possui os widgets
    """
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setup_view()
        self.transform = WindowTransformation()
        self.display_file = DisplayFile()

        self.addObjectButton.clicked.connect(self.show_dialog)
        
        self.zoomInButton.clicked.connect(self.zoom_in)
        self.zoomOutButton.clicked.connect(self.zoom_out)

        self.translateLeftButton.clicked.connect(self.translate_left)
        self.translateRightButton.clicked.connect(self.translate_right)
        self.translateUpButton.clicked.connect(self.translate_up)
        self.translateDownButton.clicked.connect(self.translate_down)

    def setup_view(self):
        uic.loadUi("UI/MainWindow.ui", self) #carrega o arquivo de interface gráfica para a janela do qt
        self.setWindowTitle("Sistema básico interativo - Computação gráfica")

        self.container = self.labelContainerForCanvas
        self.canvas = QtGui.QPixmap(531, 511)
        self.canvas.fill(QtCore.Qt.GlobalColor.white)
        self.container.setPixmap(self.canvas)

    def show_dialog(self):
        dialog = Dialog()
        dialog.show()
        dialog.exec()
        
        if dialog.inserted_type == Tipo.SEGMENTO_RETA:
            name = dialog.lineEdit.text()
            self.listOfCurrentObjects.addItems([name])
            self.display_file.array.append(dialog.object)
            self.draw_line(dialog.object)

    def render(self):
        self.canvas.fill(QtCore.Qt.GlobalColor.white)
        for item in self.display_file.array:
            if isinstance(item, Ponto):
                self.draw_point(item)
            elif isinstance(item, Reta):
                self.draw_line(item)

    def draw_line(self, line: Reta):
        painter = QtGui.QPainter(self.canvas)

        x1 = line.pontos[0].coordenadas[0]
        y1 = line.pontos[0].coordenadas[1]
        x2 = line.pontos[1].coordenadas[0]
        y2 = line.pontos[1].coordenadas[1]

        painter.drawLine(x1, y1, x2, y2)
        painter.end()
        self.container.setPixmap(self.canvas)

    def draw_point(self, point: Ponto):
        painter = QtGui.QPainter(self.canvas)

        x = point.coordenadas[0]
        y = point.coordenadas[1]

        painter.drawPoint(x, y)
        painter.end()
        self.container.setPixmap(self.canvas)

    def zoom_in(self):
        for item in self.display_file.array:
            item.zoom_in()
        self.render()
    
    def zoom_out(self):
        for item in self.display_file.array:
            item.zoom_out()
        self.render()
    
    def translate_left(self):
        for item in self.display_file.array:
            item.translate_left()
        self.render()
        
    def translate_right(self):
        for item in self.display_file.array:
            item.translate_right()
        self.render()

    def translate_up(self):
        for item in self.display_file.array:
            item.translate_up()
        self.render()

    def translate_down(self):
        for item in self.display_file.array:
            item.translate_down()
        self.render()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    window = MainWindow()    
    window.show()
    sys.exit(app.exec())
