from objeto import Objeto, Tipo
from Ponto import Ponto


class Reta(Objeto):
    def __init__(self, nome: str, pontos: tuple[Ponto, Ponto]) -> None:
        super().__init__(nome, Tipo.SEGMENTO_RETA)
        self.pontos = pontos


    def zoom(self,  scale):
        self.translate(-265, -255)

        coordenadas1 = self.pontos[0].coordenadas
        x1, y1 = coordenadas1[0], coordenadas1[1]
        self.pontos[0].coordenadas = self.scale((x1, y1), scale, scale)

        coordenadas2 = self.pontos[1].coordenadas
        x2, y2 = coordenadas2[0], coordenadas2[1]
        self.pontos[1].coordenadas = self.scale((x2, y2), scale, scale)

        self.translate(265, 255)

    def translate(self, dx, dy):
        coordenadas1 = self.pontos[0].coordenadas
        x1, y1 = coordenadas1[0], coordenadas1[1]
        self.pontos[0].coordenadas = self.translate((x1, y1), dx, dy)

        coordenadas2 = self.pontos[1].coordenadas
        x2, y2 = coordenadas2[0], coordenadas2[1]
        self.pontos[1].coordenadas = self.translate((x2, y2), dx, dy)
