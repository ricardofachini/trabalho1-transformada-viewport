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
    
    def zoom_in(self):
        self.zoom(1.1)
    
    def zoom_out(self):
        self.zoom(0.9)
    
    def zoom(self,  scale):
        coordenadas1 = self.pontos[0].coordenadas
        x1, y1 = coordenadas1[0], coordenadas1[1]
        self.pontos[0].coordenadas = self.transform.scale((x1, y1), scale, scale)

        coordenadas2 = self.pontos[1].coordenadas
        x2, y2 = coordenadas2[0], coordenadas2[1]
        self.pontos[1].coordenadas = self.transform.scale((x2, y2), scale, scale)
    
    def translate_left(self):
        self.translate(-10, 1)
    
    def translate_right(self):
        self.translate(10, 1)

    def translate_up(self):
        self.translate(1, -10)

    def translate_down(self):
        self.translate(1, 10)

    def translate(self, scale_x, scale_y):
        coordenadas1 = self.pontos[0].coordenadas
        x1, y1 = coordenadas1[0], coordenadas1[1]
        self.pontos[0].coordenadas = self.transform.translate((x1, y1), scale_x, scale_y)

        coordenadas2 = self.pontos[1].coordenadas
        x2, y2 = coordenadas2[0], coordenadas2[1]
        self.pontos[1].coordenadas = self.transform.translate((x2, y2), scale_x, scale_y)
