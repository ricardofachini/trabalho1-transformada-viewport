from src.objeto import Objeto, Tipo
from src.Ponto import Ponto

class Reta(Objeto):
    def __init__(self, nome: str, pontos: tuple[Ponto, Ponto], cor: str = "#000000") -> None:
        super().__init__(nome, Tipo.SEGMENTO_RETA, cor)
        self.pontos = pontos

        # Se não tiver nome é uma reta pertencente a um polígono.
        # Nesse caso não tem necessidade de calcular o centro.
        self.center = super().calculate_center(self.pontos)

    def zoom(self, scale, center = None):
        if center is None:
            center = self.center

        self.pontos[0].coordenadas = self.scale(self.pontos[0].coordenadas, scale, center)
        self.pontos[1].coordenadas = self.scale(self.pontos[1].coordenadas, scale, center)

    def translate(self, dx, dy):
        self.pontos[0].coordenadas = super().translate(self.pontos[0].coordenadas, dx, dy)
        self.pontos[1].coordenadas = super().translate(self.pontos[1].coordenadas, dx, dy)

        cx, cy = self.center
        self.center = super().translate((cx, cy), dx, dy)

    def rotate(self, rotation_side, rot_matrix=None, center=None):
        cx, cy = self.center if center is None else center
        
        for ponto in self.pontos:
            ponto.coordenadas = super().rotate(ponto.coordenadas, (cx, cy), rotation_side, rot_matrix)
        
        self.center = super().rotate(self.center, (cx, cy), rotation_side)
