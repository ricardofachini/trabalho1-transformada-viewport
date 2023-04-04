from src.objeto import Objeto, Tipo, RotateSide
from src.Reta import Reta
from src.Ponto import Ponto

from math import sin, radians

class WireFrame(Objeto):
    def __init__(self, nome: str, center: tuple, n_linhas: int, tam_linhas: int, cor: str = "#000000") -> None:
        super().__init__(nome, Tipo.POLIGONO, cor)
        self.nome       = nome
        self.center     = center
        self.n_linhas   = n_linhas
        self.tam_linhas = tam_linhas
        self.retas      = []
        self.points     = []
        self.calculate_lines()
        self.calculate_center()
    
    def calculate_lines(self):
        total_angle  = (self.n_linhas - 2) * 180
        single_angle = total_angle / self.n_linhas
        center_single_angle = 360 / self.n_linhas

        # Lei dos senos (dois ângulos e uma reta)
        radius = ((self.tam_linhas) * (sin(radians(single_angle / 2)))) / sin(radians(center_single_angle))
        radius = (int) (radius)

        self.calculate_points(radius, center_single_angle)

        center_x = self.center[0]
        center_y = self.center[0]
        for i in range(self.n_linhas):
            x1, y1 = self.points[i]
            x2, y2 = self.points[i + 1]
            
            p1 = Ponto('', (x1 + center_x, y1 + center_y))
            p2 = Ponto('', (x2 + center_x, y2 + center_y))

            self.retas.append(Reta('', (p1, p2), self.cor))
    
    def calculate_points(self, radius: int, angle: float):
        self.points.append((radius / 2, radius / 2))

        for i in range(self.n_linhas):
            point = super().rotate(self.points[i], self.center, RotateSide.RIGHT, angle)
            self.points.append(point)

    def zoom(self, scale):
        center_x = self.center[0]
        center_y = self.center[1]
        center = (center_x, center_y)
        for reta in self.retas:
            reta.zoom(scale, center)
    
    def translate(self, dx, dy):
        for reta in self.retas:
            reta.translate(dx, dy)
        self.center = (self.center[0] + dx, self.center[1] + dy)

    def rotate(self, rotation_side, center=None):
        if center is None:
            center = self.center

        for reta in self.retas:
            reta.rotate(rotation_side, center)
        
        self.calculate_center()
    
    def calculate_center(self):
        pontos = []
        for reta in self.retas:
            for ponto in reta.pontos:
                pontos.append(ponto)
        self.center = super().calculate_center(pontos)
