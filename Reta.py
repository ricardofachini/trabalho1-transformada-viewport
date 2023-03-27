from objeto import Objeto, Tipo
from Ponto import Ponto
#from decimal import *

#from window import WindowTransformation

class Reta(Objeto):
    def __init__(self, nome: str, pontos: tuple[Ponto, Ponto], cor: str = "#000000") -> None:
        super().__init__(nome, Tipo.SEGMENTO_RETA)
        self.pontos = pontos
        self.cor = cor


    def zoom(self, scale, centro = None):
        if centro is None:
            centro = self.calculate_center(self.pontos)
        self.line_translate(-centro[0], -centro[1])

        coordenadas1 = self.pontos[0].coordenadas
        x1, y1 = coordenadas1[0], coordenadas1[1]
        self.pontos[0].coordenadas = self.scale((x1, y1), scale, scale)

        coordenadas2 = self.pontos[1].coordenadas
        x2, y2 = coordenadas2[0], coordenadas2[1]
        self.pontos[1].coordenadas = self.scale((x2, y2), scale, scale)

        self.line_translate(centro[0], centro[1])

    def line_translate(self, dx, dy):
        coordenadas1 = self.pontos[0].coordenadas
        x1, y1 = coordenadas1[0], coordenadas1[1]
        self.pontos[0].coordenadas = self.translate((x1, y1), dx, dy)

        coordenadas2 = self.pontos[1].coordenadas
        x2, y2 = coordenadas2[0], coordenadas2[1]
        self.pontos[1].coordenadas = self.translate((x2, y2), dx, dy)
