from enum import Enum

class Tipo(Enum):
    PONTO = "PONTOS"
    SEGMENTO_RETA = "RETA"
    POLIGONO = "POLIGONO"

class Objeto:
    def __init__(self, nome: str, tipo: Tipo, coordenadas: list[tuple[float]]) -> None:
        self.nome = nome
        self.tipo = tipo
        self.coord = coordenadas
