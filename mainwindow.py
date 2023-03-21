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



class UIWindow(QtWidgets.QMainWindow):
    """
    Janela principal do qt que possui os widgets
    """
    def __init__(self, *args, **kwargs):
        super(UIWindow, self).__init__(*args, **kwargs)
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

        reta1 = Reta('Linha1', (Ponto('', (100, 100)), Ponto('', (200, 200))))
        reta2 = Reta('Linha2', (Ponto('', (50, 50)), Ponto('', (200, 50))))
        self.draw_line(reta1)
        self.display_file.array.append(reta1)
        self.draw_line(reta2)
        self.display_file.array.append(reta2)

        poligono = WireFrame('Poligono', Ponto('', (250, 250)), 8, 200)
        self.draw_polygon(poligono)

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
        
        if dialog.inserted_type:
            name = dialog.lineEdit.text()
            self.listOfCurrentObjects.addItems([name])
            self.display_file.array.append(dialog.object)
            
            if dialog.inserted_type == Tipo.PONTO:
                self.draw_point(dialog.object)
            if dialog.inserted_type == Tipo.SEGMENTO_RETA:                
                self.draw_line(dialog.object)
            if dialog.inserted_type == Tipo.POLIGONO:
                self.draw_polygon(dialog.object)

    def render(self):
        self.canvas.fill(QtCore.Qt.GlobalColor.white)
        for item in self.display_file.array:
            if isinstance(item, Ponto):
                self.draw_point(item)
            elif isinstance(item, Reta):
                self.draw_line(item)

    def draw_point(self, point: Ponto):
        painter = QtGui.QPainter(self.canvas)

        x = point.coordenadas[0]
        y = point.coordenadas[1]

        painter.drawPoint(x, y)
        painter.end()
        self.container.setPixmap(self.canvas)
    
    def draw_line(self, line: Reta):
        painter = QtGui.QPainter(self.canvas)

        x1 = (int) (line.pontos[0].coordenadas[0])
        y1 = (int) (line.pontos[0].coordenadas[1])
        x2 = (int) (line.pontos[1].coordenadas[0])
        y2 = (int) (line.pontos[1].coordenadas[1])

        painter.drawLine(x1, y1, x2, y2)
        painter.end()
        self.container.setPixmap(self.canvas)
    
    def draw_polygon(self, polygon: WireFrame):
        for line in polygon.retas:
            self.draw_line(line)

    def zoom_in(self):
        self.zoom(1.1)
    
    def zoom_out(self):
        self.zoom(0.9)
    
    def zoom(self, scale):
        for item in self.display_file.array:
            item.zoom(scale)
        self.render()
    
    def translate_left(self):
        self.translate(-10, 0)
    
    def translate_right(self):
        self.translate(10, 0)

    def translate_up(self):
        self.translate(0, -10)

    def translate_down(self):
        self.translate(0, 10)
    
    def translate(self, dx, dy):
        for item in self.display_file.array:
            item.translate(dx, dy)
        self.render()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    window = UIWindow()    
    window.show()
    sys.exit(app.exec())
