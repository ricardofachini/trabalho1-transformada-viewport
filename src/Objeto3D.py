from src.Ponto3D import Ponto3D


class Objeto3D():
    def __init__(self, nome: str, wireframe: [tuple[Ponto3D]]):
        self.nome = nome
        self.segmentos_de_reta = wireframe
