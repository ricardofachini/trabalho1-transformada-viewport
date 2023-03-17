from enum import Enum

class Tipo(Enum):
    PONTO = "PONTO"
    SEGMENTO_RETA = "RETA"
    POLIGONO = "POLIGONO"

class Objeto:
    def __init__(self, nome: str, tipo: Tipo) -> None:
        self.nome = nome
        self.tipo = tipo
