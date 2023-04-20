# This Python file uses the following encoding: utf-8
import sys
import numpy as np
from PyQt6 import uic, QtWidgets, QtGui, QtCore

from src.constants import TRANSLATION_STEP, ZOOM_IN_SCALE, ZOOM_OUT_SCALE, ROTATION_LEFT, ROTATION_RIGHT, BORDER_SIZE

import images_rcc

from dialog import Dialog
from src.objeto import Tipo, RotateSide

from src.window import Window
from src.objdescriptor import ObjDescriptor

from src.Ponto import Ponto
from src.Reta import Reta
from src.Poligono import WireFrame
from src.Vertice import Vertice


class UIWindow(QtWidgets.QMainWindow):
    """
    Janela principal do qt que possui os widgets e a viewport
    """
    def __init__(self, *args, **kwargs):
        super(UIWindow, self).__init__(*args, **kwargs)
        self.setup_view()

        # coordenadas maximas e minimas da viewport
        self.minXvp = 0
        self.minYvp = 0
        self.maxXvp = (int)(self.labelContainerForCanvas.width())
        self.maxYvp = (int)(self.labelContainerForCanvas.height())
        self.vp_width = self.maxXvp - self.minXvp
        self.vp_height = self.maxYvp - self.minYvp

        self.window = Window()
        self.display_file = []
        self.obj_descriptor = ObjDescriptor()

        self.selected_object = None
        self.selected_index = 0

        self.display_file.append(None)
        self.listOfCurrentObjects.addItems(['<None>'])

        # listeners dos botões da interface
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

        self.draw_border()

        # PARA TESTE
        bd = BORDER_SIZE
        world_coords = (self.minXvp + bd, self.maxXvp - bd, self.minYvp + bd, self.maxYvp - bd)
        reta = Reta(
            "reta1",
            (Vertice(-330, 0),
             Vertice(-300, 200)
             )
        )
        reta.align_center(self.window.center)
        reta.draw(self.canvas, self.container, self.get_vp_coords(reta.pontos[0].world_coordinates), 
                  self.get_vp_coords(reta.pontos[1].world_coordinates), world_coords)
        self.display_file.append(reta)
        self.listOfCurrentObjects.addItems([reta.nome])
        poligono200 = WireFrame('Poligono200', (0, 0), 8, 200)
        poligono300 = WireFrame('Poligono300', (0, 0), 8, 300)
        poligono200.align_center(self.window.center)
        poligono300.align_center(self.window.center)
        poligono200.draw(self.canvas, self.container, self.get_vp_coords, world_coords)
        self.display_file.append(poligono200)
        self.listOfCurrentObjects.addItems(['Polígono200'])
        poligono300.draw(self.canvas, self.container, self.get_vp_coords, world_coords)
        self.display_file.append(poligono300)
        self.listOfCurrentObjects.addItems(['Polígono300'])

    def setup_view(self):
        uic.loadUi("UI/MainWindow.ui", self)  # carrega o arquivo de interface gráfica para a janela do qt
        self.setWindowTitle("Sistema básico interativo - Computação gráfica")

        self.container = self.labelContainerForCanvas
        self.canvas = QtGui.QPixmap(531, 511)  # cria o canvas (viewport)
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
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Abrir arquivo', './', "Wavefront .obj (*.obj)")
        objects = self.obj_descriptor.import_file(file_path)
        for item in objects:
            self.display_file.append(item)
            self.listOfCurrentObjects.addItems([item.nome])
            
            if item.tipo == Tipo.SEGMENTO_RETA:
                self.draw_line(item)
            elif item.tipo == Tipo.PONTO:
                self.draw_point(item)
            elif item.tipo == Tipo.POLIGONO:
                self.draw_polygon(item)

    def on_export_file_click(self):
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Exportar arquivo', "./", "Wavefront .obj (*.obj)")
        file_name = QtCore.QFileInfo(file_path).fileName()
        for item in self.display_file:
            if item is not None:
                self.obj_descriptor.transform_to_wavefront(item)
        self.obj_descriptor.export_file(file_path, file_name)

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

            dialog.object.align_center(self.window.center)

            if dialog.inserted_type == Tipo.PONTO:
                item = dialog.object
                x, y = self.get_vp_coords(item.coordenadas.world_coordinates)                
                item.draw(self.canvas, self.container, (self.minXvp, self.maxXvp, self.minYvp, self.maxYvp), (x, y))
            if dialog.inserted_type == Tipo.SEGMENTO_RETA:
                item = dialog.object
                x1, y1 = self.get_vp_coords(item.pontos[0].world_coordinates)
                x2, y2 = self.get_vp_coords(item.pontos[1].world_coordinates)

                item.draw(self.canvas, self.container, (x1, y1), (x2, y2))
            if dialog.inserted_type == Tipo.POLIGONO:
                dialog.object.draw(self.canvas, self.container, self.get_vp_coords)

    def render(self):
        self.canvas.fill(QtCore.Qt.GlobalColor.white)

        bd = BORDER_SIZE
        world_coords = (self.minXvp + bd, self.maxXvp - bd, self.minYvp + bd, self.maxYvp - bd)
        for item in self.display_file:
            if isinstance(item, Ponto):
                x, y = self.get_vp_coords(item.coordenadas.world_coordinates)                
                item.draw(self.canvas, self.container, (self.minXvp, self.maxXvp, self.minYvp, self.maxYvp), (x, y))
            elif isinstance(item, Reta):
                x1, y1 = self.get_vp_coords(item.pontos[0].world_coordinates)
                x2, y2 = self.get_vp_coords(item.pontos[1].world_coordinates)
                item.draw(self.canvas, self.container, (x1, y1), (x2, y2), world_coords)
            elif isinstance(item, WireFrame):
                item.draw(self.canvas, self.container, self.get_vp_coords, world_coords)
        
        self.draw_border()

    def draw_border(self):
        pen = QtGui.QPen(QtGui.QColor('black'))
        pen.setWidth(2)

        painter = QtGui.QPainter(self.canvas)
        painter.setPen(pen)
        
        # Vertical Left (vl) / Horizontal Up (hu) / Vertical Right (vr) / Horizontal Down (hd)
        bd = BORDER_SIZE
        vlx1, vly1, vlx2, vly2 = bd, bd, bd, (self.vp_height - bd)
        hux1, huy1, hux2, huy2 = bd, bd, (self.vp_width - bd), bd
        vrx1, vry1, vrx2, vry2 = (self.vp_width - bd), bd, (self.vp_width - bd), (self.vp_height - bd)
        hdx1, hdy1, hdx2, hdy2 = (self.vp_width - bd), (self.vp_height - bd), bd, (self.vp_height - bd)

        painter.drawLine(vlx1, vly1, vlx2, vly2)
        painter.drawLine(hux1, huy1, hux2, huy2)
        painter.drawLine(vrx1, vry1, vrx2, vry2)
        painter.drawLine(hdx1, hdy1, hdx2, hdy2)
        painter.end()
        self.container.setPixmap(self.canvas)

    def get_vp_coords(self, coords):
        x = (int)(self.window.get_x_to_viewport(coords[0], self.vp_width))
        y = (int)(self.window.get_y_to_viewport(coords[1], self.vp_height))

        return (x, y)

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
        self.window.scale(scale)

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
        self.window.translate(dx, dy)  # move a window

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
        else:
            self.rotate_window(RotateSide.LEFT)

        self.render()

    def rotate_right(self):
        if (self.selected_object is not None):
            self.rotate(RotateSide.RIGHT)
        else:
            self.rotate_window(RotateSide.RIGHT)

        self.render()

    def rotate(self, rotation_side):
        center = None

        if self.radioWindow.isChecked():
            center = (self.window.centerX, self.window.centerY)
        elif self.radioOther.isChecked():
            center = ((int)(self.spinBoxCenX.text()), (int)(self.spinBoxCenY.text()))

        self.selected_object.rotate(rotation_side, center)

    def rotate_window(self, rotation_side):
        # self.window.rotate(rotation_side)
        rot_matrix = ROTATION_LEFT if rotation_side == RotateSide.LEFT else ROTATION_RIGHT
        
        center_x, center_y = self.window.center
        to_window_center = np.array([[1, 0, 0], [0, 1, 0], [-center_x, -center_y, 1]])
        to_own_center    = np.array([[1, 0, 0], [0, 1, 0], [center_x, center_y, 1]])

        rot_matrix = to_window_center @ rot_matrix @ to_own_center
        
        for item in self.display_file:
            if item is not None:
                item.rotate(rotation_side, self.window.center, rot_matrix)

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
