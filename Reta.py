from objeto import Objeto, Tipo
from Ponto import Ponto

from windowtransformation import WindowTransformation

class Reta(Objeto):
    def __init__(self, nome: str, pontos: tuple) -> None:
        if len(pontos) != 2:
            raise Exception('Para criar uma reta são necessários dois, e apenas dois, pontos.')
        super().__init__(nome, Tipo.SEGMENTO_RETA, pontos)
        self.pontos = pontos

        self.transform = WindowTransformation()
    
    def zoom(self,  scale):
        coordenadas1 = self.pontos[0].coordenadas
        x1, y1 = coordenadas1[0], coordenadas1[1]
        self.pontos[0].coordenadas = self.transform.scale((x1, y1), scale, scale)

        coordenadas2 = self.pontos[1].coordenadas
        x2, y2 = coordenadas2[0], coordenadas2[1]
        self.pontos[1].coordenadas = self.transform.scale((x2, y2), scale, scale)

    def translate(self, dx, dy):
        coordenadas1 = self.pontos[0].coordenadas
        x1, y1 = coordenadas1[0], coordenadas1[1]
        self.pontos[0].coordenadas = self.transform.translate((x1, y1), dx, dy)

        coordenadas2 = self.pontos[1].coordenadas
        x2, y2 = coordenadas2[0], coordenadas2[1]
        self.pontos[1].coordenadas = self.transform.translate((x2, y2), dx, dy)
