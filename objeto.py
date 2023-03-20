from enum import Enum

class Tipo(Enum):
    """
    os tipos de objetos que o sistema suporta
    """
    PONTO = "PONTO"
    SEGMENTO_RETA = "RETA"
    POLIGONO = "POLIGONO"

class Objeto:
    """
    Classe genérica para um objeto qualquer
    """
    def __init__(self, nome: str, tipo: Tipo, pontos: tuple[int, int]) -> None:
        self.nome = nome
        self.tipo = tipo
        self.pontos = pontos
        #self.centro = self.calculate_center()

    def calculate_center(self) -> tuple[int, int]:
        """
        Calcula o centro de um objeto com base em seus vértices

        @return (tuple[int, int]): (Cx, Cy)
        """
        n = len(self.pontos)
        cx = 0
        cy = 0
        for i in range(n):
            cx += self.pontos[i].coordenadas[0]
        for i in range(n):
            cy += self.pontos[i].coordenadas[1]
        cx = cx/n
        cy = cy/n
        return (int(cx), int(cy))
