# This Python file uses the following encoding: utf-8
import sys
from PyQt6 import uic, QtWidgets, QtGui, QtCore

import images_rcc

from dialog import Dialog
from objeto import Tipo

from window import Window
from displayfile import DisplayFile

from Ponto import Ponto
from Reta import Reta
from Poligono import WireFrame


class UIWindow(QtWidgets.QMainWindow):
    """
    Janela principal do qt que possui os widgets e a viewport
    """
    def __init__(self, *args, **kwargs):
        super(UIWindow, self).__init__(*args, **kwargs)
        #coordenadas maximas e minimas da viewport
        self.minXvp = 0
        self.minYvp = 0
        self.maxXvp = 531
        self.maxYvp = 511

        self.setup_view()
        self.WorldWindow = Window()
        self.display_file = DisplayFile()

        #listeners dos botões da interface
        self.addObjectButton.clicked.connect(self.show_dialog)
        
        self.zoomInButton.clicked.connect(self.zoom_in)
        self.zoomOutButton.clicked.connect(self.zoom_out)

        self.translateLeftButton.clicked.connect(self.translate_left)
        self.translateRightButton.clicked.connect(self.translate_right)
        self.translateUpButton.clicked.connect(self.translate_up)
        self.translateDownButton.clicked.connect(self.translate_down)

        # PARA TESTE
        # reta1 = Reta('Linha1', (Ponto('', (100, 100)), Ponto('', (200, 200))))
        # reta2 = Reta('Linha2', (Ponto('', (50, 50)), Ponto('', (200, 50))))
        # poligono = WireFrame('Poligono', Ponto('', (250, 250)), 8, 200)
        
        # self.draw_line(reta1)
        # self.display_file.array.append(reta1)
        # self.listOfCurrentObjects.addItems(['Reta1'])
        
        # self.draw_line(reta2)
        # self.display_file.array.append(reta2)
        # self.listOfCurrentObjects.addItems(['Reta2'])

        # self.draw_polygon(poligono)
        # self.display_file.array.append(poligono)
        # self.listOfCurrentObjects.addItems(['Polígono'])

    def setup_view(self):
        uic.loadUi("UI/MainWindow.ui", self) #carrega o arquivo de interface gráfica para a janela do qt
        self.setWindowTitle("Sistema básico interativo - Computação gráfica")

        self.container = self.labelContainerForCanvas
        self.canvas = QtGui.QPixmap(531, 511) #cria o canvas (viewport)
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

    #transformadas de viewport
    def get_x_to_viewport(self, x_window):
        return ((x_window - self.WorldWindow.minXwp) / (self.WorldWindow.maxXwp - self.WorldWindow.minXwp)) * (self.maxXvp - self.minXvp)
    
    def get_y_to_viewport(self, y_window):
        return (1 - ((y_window - self.WorldWindow.minYwp) / (self.WorldWindow.maxYwp - self.WorldWindow.minYwp))) * (self.maxYvp - self.minYvp)

    def render(self):
        self.canvas.fill(QtCore.Qt.GlobalColor.white)
        for item in self.display_file.array:
            if isinstance(item, Ponto):
                self.draw_point(item)
            elif isinstance(item, Reta):
                self.draw_line(item)
            elif isinstance(item, WireFrame):
                self.draw_polygon(item)

    def draw_point(self, point: Ponto):
        painter = QtGui.QPainter(self.canvas)

        x = point.coordenadas[0]
        x = int(self.get_x_to_viewport(x))
        y = point.coordenadas[1]
        y = int(self.get_y_to_viewport(y))

        painter.drawPoint(x, y)
        painter.end()
        self.container.setPixmap(self.canvas)
    
    def draw_line(self, line: Reta):
        pen = QtGui.QPen(QtGui.QColor(line.cor))
        pen.setWidth(2)

        painter = QtGui.QPainter(self.canvas)        
        painter.setPen(pen)

        x1 = (int) (self.get_x_to_viewport(line.pontos[0].coordenadas[0]))

        y1 = (int) (self.get_y_to_viewport(line.pontos[0].coordenadas[1]))

        x2 = (int) (self.get_x_to_viewport(line.pontos[1].coordenadas[0]))

        y2 = (int) (self.get_y_to_viewport(line.pontos[1].coordenadas[1]))

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
        self.WorldWindow.translate(-self.WorldWindow.centerX, -self.WorldWindow.centerY)
        self.WorldWindow.scale(scale)
        self.WorldWindow.translate(self.WorldWindow.centerX, self.WorldWindow.centerY)
        self.render()
    
    def translate_left(self):
        self.translate(20, 0)
    
    def translate_right(self):
        self.translate(-20, 0)

    def translate_up(self):
        self.translate(0, -20)

    def translate_down(self):
        self.translate(0, 20)
    
    def translate(self, dx, dy):
        self.WorldWindow.translate(dx, dy) #move a window
        self.render()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    window = UIWindow()    
    window.show()
    sys.exit(app.exec())
