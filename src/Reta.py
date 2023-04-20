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

    def draw(self, canvas, container, p1_coords, p2_coords, world_coords):
        x1, y1 = p1_coords
        x2, y2 = p2_coords
        clipping_points = self.check_clipping(x1, y1, x2, y2, world_coords)

        if clipping_points is None:
            return

        x1, y1, x2, y2 = clipping_points
        pen = QtGui.QPen(QtGui.QColor(self.cor))
        pen.setWidth(2)

        painter = QtGui.QPainter(canvas)
        painter.setPen(pen)
        
        if not all([x1, y1, x2, y2]):
            return
        
        painter.drawLine(x1, y1, x2, y2)
        painter.end()
        container.setPixmap(canvas)

    def check_clipping(self, x1, y1, x2, y2, world_coords):
        minx, maxx, miny, maxy = world_coords
        
        #         acima      abaixo     direita    esquerda
        quad1 = (y1 < miny, y1 > maxy, x1 > maxx, x1 < minx)
        quad2 = (y2 < miny, y2 > maxy, x2 > maxx, x2 < minx)

        result = (quad1[i] and quad2[i] for i in range(4))
        
        if any(result):
            return None
        
        if (quad1 == quad2) and (not any(result)):
            return x1, y1, x2, y2

        # Se a linha foi cortada, calcular os pontos de interseção e desenhar a nova linha cortada
        dx, dy = (x2 - x1), (y2 - y1)
        if dx == 0:
            if y1 < miny:
                y1 = miny
            elif y1 > maxy:
                y1 = maxy
            return x1, y1

        m = dy / dx

        clip1 = self.clip_point(world_coords, x1, y1, quad1, m)
        if clip1 is None:
            return None
        
        x1, y1 = clip1
        x2, y2 = self.clip_point(world_coords, x2, y2, quad2, m)
        
        return x1, y1, x2, y2
    
    def clip_point(self, world_coords, x, y, quad, m):
        if not any(quad):
            return x, y

        minx, maxx, miny, maxy = world_coords
        for i, p in enumerate(quad):
            if p:
                if i == 0:  # acima
                    x = x + (1 / m) * (miny - y)
                    y = miny
                    return x, y if ((x > minx) and (x < maxx)) else None
                elif i == 1:  # abaixo
                    x = x + (1 / m) * (maxy - y)
                    y = maxy
                    return x, y if ((x > minx) and (x < maxx)) else None
                elif i == 2:  # direita
                    y = (m * (maxx - x)) + y
                    x = maxx
                    return x, y if ((y > miny) and (y < maxy)) else None
                else:  # esquerda
                    y = (m * (minx - x)) + y
                    x = minx
                    return x, y if ((y > miny) and (y < maxy)) else None
