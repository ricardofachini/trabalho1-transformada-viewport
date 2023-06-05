from src.Ponto3D import Ponto3D


class Reta3D():
    def __init__(self, nome: str = '', pontos: list = [Ponto3D, Ponto3D]) -> None:
        self.nome = nome
        self.pontos = pontos

    def translate(self, matrix=[]):
        for ponto in self.pontos:
            ponto.translate(matrix)
