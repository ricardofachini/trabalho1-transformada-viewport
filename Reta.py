from objeto import Objeto, Tipo
from Ponto import Ponto

class Reta(Objeto):
    def __init__(self, nome: str, pontos: tuple[Ponto, Ponto]) -> None:
        super().__init__(nome, Tipo.SEGMENTO_RETA)
        self.pontos = pontos
        self.center = super().calculate_center(self.pontos)


    def zoom(self, scale, center = None):
        if center is None:
            center = self.center
        self.translate(-center[0], -center[1])

        coordenadas1 = self.pontos[0].coordenadas
        x1, y1 = coordenadas1[0], coordenadas1[1]
        self.pontos[0].coordenadas = self.scale((x1, y1), scale, scale)

        coordenadas2 = self.pontos[1].coordenadas
        x2, y2 = coordenadas2[0], coordenadas2[1]
        self.pontos[1].coordenadas = self.scale((x2, y2), scale, scale)

        self.translate(center[0], center[1])

    def translate(self, dx, dy):
        x1, y1 = self.pontos[0].coordenadas
        self.pontos[0].coordenadas = super().translate((x1, y1), dx, dy)

        x2, y2 = self.pontos[1].coordenadas
        self.pontos[1].coordenadas = super().translate((x2, y2), dx, dy)

        cx, cy = self.center
        self.center = super().translate((cx, cy), dx, dy)

    def rotate(self, angle, center=None):
        cx, cy = self.center if center is None else center
        
        self.translate(-cx, -cy)
        for ponto in self.pontos:
            ponto.coordenadas = super().rotate(ponto.coordenadas, angle)
        self.center = super().rotate(self.center, angle)
        self.translate(cx, cy)
    
    # def calculate_center(self):
    #     x1, y1 = self.pontos[0].coordenadas
    #     x2, y2 = self.pontos[1].coordenadas

    #     x_min = min(x1, x2)
    #     y_min = min(y1, y2)

    #     dx = abs(x1 - x2) / 2
    #     dy = abs(y1 - y2) / 2

    #     self.center = (x_min + dx, y_min + dy)
