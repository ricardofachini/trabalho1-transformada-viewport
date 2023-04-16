from src.objeto import Objeto, Tipo, RotateSide
from src.Reta import Reta
from src.Vertice import Vertice

from math import sin, cos, pi, radians

class WireFrame(Objeto):
    def __init__(self, nome: str, center: tuple, n_linhas: int, tam_linhas: int, cor: str = "#000000", pontos=None) -> None:
        super().__init__(nome, Tipo.POLIGONO, cor)
        self.nome       = nome
        self.center     = center
        self.n_linhas   = n_linhas
        self.tam_linhas = tam_linhas
        self.retas      = []
        if pontos is None:
            pontos = []
        self.points     = pontos

        self.calculate_lines()
    
    def calculate_lines(self):
        # Calcula o raio do polígono
        radius = self.tam_linhas / (2 * sin(radians(360 / self.n_linhas)))
        if len(self.points) == 0:
            self.calculate_points(radius)

        for i in range(self.n_linhas):
            x1, y1 = self.points[i]
            x2, y2 = self.points[i + 1]
            
            p1 = Vertice(x1, y1)
            p2 = Vertice(x2, y2)

            self.retas.append(Reta('', (p1, p2), self.cor))
    
    def calculate_points(self, radius: int):
        angle = 2 * pi / self.n_linhas

        for i in range(self.n_linhas + 1):
            x = radius * cos(i * angle)
            y = radius * sin(i * angle)
            self.points.append((x + self.center[0], y + self.center[1]))

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

    def rotate(self, rotation_side, center=None, rot_matrix=None):
        if center is None:
            center = self.center

        for reta in self.retas:
            reta.rotate(rotation_side, center, rot_matrix)
        
        self.calculate_center()
    
    def calculate_center(self):
        pontos = []
        for reta in self.retas:
            for ponto in reta.pontos:
                pontos.append(ponto)
        self.center = super().calculate_center(pontos)
