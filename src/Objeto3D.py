from src.Ponto3D import Ponto3D


class Objeto3D():
    def __init__(self, nome: str, retas: list = [Ponto3D, Ponto3D]):
        self.nome = nome
        self.retas = retas
