from src.objeto import Objeto, Tipo
from src.Vertice import Vertice

from PyQt6 import QtGui


class Reta(Objeto):
    def __init__(self, nome: str, pontos: tuple[Vertice, Vertice], cor: str = "#000000") -> None:
        super().__init__(nome, Tipo.SEGMENTO_RETA, cor)
        self.pontos = pontos

        # Se não tiver nome é uma reta pertencente a um polígono.
        # Nesse caso não tem necessidade de calcular o centro.
        self.center = super().calculate_center(self.pontos)

    def zoom(self, scale, center=None):
        if center is None:
            center = self.center

        self.pontos[0].world_coordinates = self.scale(self.pontos[0].world_coordinates, scale, center)
        self.pontos[1].world_coordinates = self.scale(self.pontos[1].world_coordinates, scale, center)

    def translate(self, dx, dy):
        self.pontos[0].world_coordinates = super().translate(self.pontos[0].world_coordinates, dx, dy)
        self.pontos[1].world_coordinates = super().translate(self.pontos[1].world_coordinates, dx, dy)

        cx, cy = self.center
        self.center = super().translate((cx, cy), dx, dy)

    def rotate(self, rotation_side, center=None, rot_matrix=None):
        cx, cy = self.center if center is None else center

        for ponto in self.pontos:
            ponto.world_coordinates = super().rotate(ponto.world_coordinates, (cx, cy), rotation_side, rot_matrix)

        self.center = super().rotate(self.center, (cx, cy), rotation_side)

    def draw(self, canvas, container, p1_coords, p2_coords):
        pen = QtGui.QPen(QtGui.QColor(self.cor))
        pen.setWidth(2)

        painter = QtGui.QPainter(canvas)
        painter.setPen(pen)

        x1, y1 = p1_coords
        x2, y2 = p2_coords
        painter.drawLine(x1, y1, x2, y2)
        painter.end()
        container.setPixmap(canvas)
