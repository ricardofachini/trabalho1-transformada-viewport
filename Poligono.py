from objeto import Objeto, Tipo
from Reta import Reta
from Ponto import Ponto


from math import sin, radians

class WireFrame(Objeto):
    def __init__(self, nome: str, centro: Ponto, n_linhas: int, tam_linhas: int, retas: list[Reta]=[]) -> None:
        super().__init__(nome, Tipo.POLIGONO)
        self.nome       = nome
        self.centro     = centro
        self.n_linhas   = n_linhas
        self.tam_linhas = tam_linhas
        self.retas      = retas
        self.points     = []
        self.calculate_lines()
    
    def calculate_lines(self):
        total_angle  = (self.n_linhas - 2) * 180
        single_angle = total_angle / self.n_linhas
        center_single_angle = 360 / self.n_linhas

        # Lei dos senos (dois ângulos e uma reta)
        radius = ((self.tam_linhas) * (sin(radians(single_angle / 2)))) / sin(radians(center_single_angle))
        radius = (int) (radius)

        self.calculate_points(radius, center_single_angle)

        centro_x = self.centro.coordenadas[0]
        centro_y = self.centro.coordenadas[1]
        for i in range(self.n_linhas):
            x1, y1 = self.points[i]
            x2, y2 = self.points[i + 1]
            
            p1 = Ponto('', (x1 + centro_x, y1 + centro_y))
            p2 = Ponto('', (x2 + centro_x, y2 + centro_y))

            self.retas.append(Reta('', (p1, p2)))
    
    def calculate_points(self, radius: int, angle: float):
        self.points.append((radius / 2, radius / 2))

        for i in range(self.n_linhas):
            point = self.rotate(self.points[i], angle)
            self.points.append(point)

    def zoom(self, scale):
        for reta in self.retas:
            reta.zoom(scale)
    
    def translate(self, dx, dy):
        for reta in self.retas:
            reta.translate(dx, dy)
   