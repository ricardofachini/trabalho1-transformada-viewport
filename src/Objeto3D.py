from src.Ponto3D import Ponto3D


class Objeto3D():
    def __init__(self, nome: str, retas: list = [Ponto3D, Ponto3D]):
        self.nome = nome
        self.retas = retas

    def rotate(self, angle):
        for ponto in self.segmentos_de_reta:
            ponto.rotate(angle)
    
    def translate(self, Tx, Ty, Tz):
        for ponto in self.segmentos_de_reta:
            ponto.translate(Tx, Ty, Tz)
    
    def scale(self, Sx, Sy, Sz):
        for ponto in self.segmentos_de_reta:
            ponto.scale(Sx, Sy, Sz)

    def draw(self):
        """Desenha o objeto com 3 dimensões"""
