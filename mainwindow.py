# This Python file uses the following encoding: utf-8
import sys
from PyQt6 import uic, QtWidgets, QtGui, QtCore

from src.constants import TRANSLATION_STEP, ZOOM_IN_SCALE, ZOOM_OUT_SCALE

import images_rcc

from dialog import Dialog
from src.objeto import Tipo

from src.window import Window
from src.objdescriptor import ObjDescriptor

from src.Ponto import Ponto
from src.Reta import Reta
from src.Poligono import WireFrame

from src.objeto import RotateSide


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
        self.display_file = []
        self.obj_descriptor = ObjDescriptor()
        
        self.selected_object = None
        self.selected_index = int

        self.display_file.append(None)
        self.listOfCurrentObjects.addItems(['<None>'])


        #listeners dos botões da interface
        self.addObjectButton.clicked.connect(self.show_dialog)
        self.listOfCurrentObjects.itemDoubleClicked.connect(self.select_current_item)
        
        self.zoomInButton.clicked.connect(self.zoom_in)
        self.zoomOutButton.clicked.connect(self.zoom_out)

        self.translateLeftButton.clicked.connect(self.translate_left)
        self.translateRightButton.clicked.connect(self.translate_right)
        self.translateUpButton.clicked.connect(self.translate_up)
        self.translateDownButton.clicked.connect(self.translate_down)

        self.radioOther.toggled.connect(self.show_center_options)
        self.radioObject.toggled.connect(self.not_show_center_options)
        self.radioWindow.toggled.connect(self.not_show_center_options)

        self.rotateLeftButton.clicked.connect(self.rotate_left)
        self.rotateRightButton.clicked.connect(self.rotate_right)

        #teste
        reta1 = Reta("teste-reta1", (Ponto("", (100, 200)), Ponto("", (200, 100))), "#938412")
        self.draw_line(reta1)
        self.listOfCurrentObjects.addItems([reta1.nome])
        self.display_file.append(reta1)

        # PARA TESTE
        reta1 = Reta('Reta1', (Ponto('', (100, 100)), Ponto('', (200, 200))))
        reta2 = Reta('Reta2', (Ponto('', (50, 50)), Ponto('', (200, 50))))
        poligono = WireFrame('Poligono', (250, 250), 8, 200)
        
        self.draw_line(reta1)
        self.display_file.append(reta1)
        self.listOfCurrentObjects.addItems(['Reta1'])
        
        self.draw_line(reta2)
        self.display_file.append(reta2)
        self.listOfCurrentObjects.addItems(['Reta2'])

        self.draw_polygon(poligono)
        self.display_file.append(poligono)
        self.listOfCurrentObjects.addItems(['Polígono'])

    def setup_view(self):
        uic.loadUi("UI/MainWindow.ui", self) #carrega o arquivo de interface gráfica para a janela do qt
        self.setWindowTitle("Sistema básico interativo - Computação gráfica")

        self.container = self.labelContainerForCanvas
        self.canvas = QtGui.QPixmap(531, 511) #cria o canvas (viewport)
        self.canvas.fill(QtCore.Qt.GlobalColor.white)
        self.container.setPixmap(self.canvas)

        self.not_show_center_options()
        self.radioObject.setChecked(True)
        self.create_menu_actions()
        self.create_menu_bar()

    def create_menu_actions(self):
        self.open_action = QtGui.QAction("&Abrir...    ", self)
        self.open_action.triggered.connect(self.on_open_file_click)
        self.export_action = QtGui.QAction("&Exportar como     ", self)
        self.export_action.setShortcut("Ctrl+S")
        self.export_action.triggered.connect(self.on_export_file_click)

    def on_open_file_click(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self, 'Abrir arquivo', './', "Wavefront .obj (*.obj)")
        print(file)

    def on_export_file_click(self):
        file_path = QtWidgets.QFileDialog.getSaveFileName(self, 'Exportar arquivo', "./", "Wavefront .obj (*.obj)" )

        for item in self.display_file:
            if item is not None:
                self.obj_descriptor.transform_to_wavefront(item)
        self.obj_descriptor.export_file(file_path)

    def create_menu_bar(self):
        menu = self.menuBar()
        file_menu = QtWidgets.QMenu("&Arquivo", self)
        menu.addMenu(file_menu)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.export_action)

    def show_dialog(self):
        dialog = Dialog()
        dialog.show()
        dialog.exec()

        if dialog.inserted_type:
            name = dialog.lineEdit.text()
            self.listOfCurrentObjects.addItems([name])
            self.display_file.append(dialog.object)
            
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
        for item in self.display_file:
            if isinstance(item, Ponto):
                self.draw_point(item)
            elif isinstance(item, Reta):
                self.draw_line(item)
            elif isinstance(item, WireFrame):
                self.draw_polygon(item)

    def draw_point(self, point: Ponto):
        pen = QtGui.QPen(QtGui.QColor(point.cor))
        pen.setWidth(2)

        painter = QtGui.QPainter(self.canvas)        
        painter.setPen(pen)

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
        if self.selected_object is None:
            self.zoom_window(ZOOM_IN_SCALE)
        else:
            self.display_file[self.selected_index].zoom(ZOOM_IN_SCALE)
    
        self.render()

    def zoom_out(self):
        if self.selected_object is None:
            self.zoom_window(ZOOM_OUT_SCALE)
        else:
            self.display_file[self.selected_index].zoom(ZOOM_OUT_SCALE)
        
        self.render()

    def zoom_window(self, scale):
        self.WorldWindow.translate(-self.WorldWindow.centerX, -self.WorldWindow.centerY)
        self.WorldWindow.scale(scale)
        self.WorldWindow.translate(self.WorldWindow.centerX, self.WorldWindow.centerY)

    def translate_left(self):
        if self.selected_object is None:
            self.translate_window(TRANSLATION_STEP, 0)
        else:
            if self.selected_object.tipo == Tipo.SEGMENTO_RETA:
                self.display_file[self.selected_index].translate(-TRANSLATION_STEP, 0)
            else:
                self.display_file[self.selected_index].translate(-TRANSLATION_STEP, 0)
        
        self.render()

    def translate_right(self):
        if self.selected_object is None:
            self.translate_window(-TRANSLATION_STEP, 0)
        else:
            if self.selected_object.tipo == Tipo.SEGMENTO_RETA:
                self.display_file[self.selected_index].translate(TRANSLATION_STEP, 0)
            else:
                self.display_file[self.selected_index].translate(TRANSLATION_STEP, 0)
        
        self.render()

    def translate_up(self):
        if self.selected_object is None:
            self.translate_window(0, -TRANSLATION_STEP)
        else:
            if self.selected_object.tipo == Tipo.SEGMENTO_RETA:
                self.display_file[self.selected_index].translate(0, TRANSLATION_STEP)
            else:
                self.display_file[self.selected_index].translate(0, TRANSLATION_STEP)
        
        self.render()

    def translate_down(self):
        if self.selected_object is None:
            self.translate_window(0, TRANSLATION_STEP)
        else:
            if self.selected_object.tipo == Tipo.SEGMENTO_RETA:
                self.display_file[self.selected_index].translate(0, -TRANSLATION_STEP)
            else:
                self.display_file[self.selected_index].translate(0, -TRANSLATION_STEP)
        
        self.render()

    def translate_window(self, dx, dy):
        self.WorldWindow.translate(dx, dy) #move a window

    def show_center_options(self):
        self.labelCenX.setVisible(True)
        self.labelCenY.setVisible(True)

        self.spinBoxCenX.setVisible(True)
        self.spinBoxCenY.setVisible(True)

    def not_show_center_options(self):
        self.labelCenX.setVisible(False)
        self.labelCenY.setVisible(False)

        self.spinBoxCenX.setVisible(False)
        self.spinBoxCenY.setVisible(False)

    def rotate_left(self):
        if (self.selected_object is not None):
            self.rotate(RotateSide.LEFT)

    def rotate_right(self):
        if (self.selected_object is not None):
            self.rotate(RotateSide.RIGHT)

    def rotate(self, rotation_side):
        center = None
        
        if self.radioWindow.isChecked():
            center = (self.WorldWindow.centerX, self.WorldWindow.centerY)
        elif self.radioOther.isChecked():
            center = ((int) (self.spinBoxCenX.text()), (int) (self.spinBoxCenY.text()))
        

        self.selected_object.rotate(rotation_side, center)
        self.render()

    def select_current_item(self, selected_item):
        self.selected_index = self.listOfCurrentObjects.row(selected_item)
        self.selected_object = self.display_file[self.selected_index]
        if self.selected_object is None:
            self.selectedObjectCurrentText.setText("Window")
        else:
            self.selectedObjectCurrentText.setText(self.selected_object.nome)
        self.selectedObjectCurrentText.setStyleSheet("font-weight: bold")
        self.render()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    window = UIWindow()    
    window.show()
    sys.exit(app.exec())
