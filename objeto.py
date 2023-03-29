from enum import Enum
from math import sin, cos, radians


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
    def __init__(self, nome: str, tipo: Tipo, cor: str = "#000000") -> None:
        self.nome = nome
        self.tipo = tipo
        self.cor = cor

    def rotate(self, coordenadas: tuple, angle) -> tuple[int, int]:
        """
        Recebe uma tupla de coordenadas 2D, e retorna a tupla rotacionada
        """
        rad = radians(angle)
        
        x = coordenadas[0] * cos(rad) - coordenadas[1] * sin(rad)
        y = coordenadas[0] * sin(rad) + coordenadas[1] * cos(rad)
        return (x, y)
    
    def scale(self, points: tuple, sx, sy) -> tuple[int, int]:
        """
        Recebe uma tupla de coordenadas 2D, e retorna a tupla escalonada
        """
        transformation_matrix = [[sx, 0, 0], [0, sy, 0], [0, 0, 1]]
        current_vector = [points[0], points[1], 1]
        x = 0
        y = 0
        for i in range(3):
            x += current_vector[i]*transformation_matrix[i][0]
        for i in range(3):
            y += current_vector[i]*transformation_matrix[i][1]
        return ((int) (x), (int) (y))
    
    def translate(self, points: tuple, dx: int, dy: int) -> tuple[int, int]:
        """
        Recebe uma tupla de coordenadas 2D, e retorna a tupla translada
        """
        return(int(points[0] + dx), int(points[1] + dy))

    def calculate_center(self, points) -> tuple[int, int]:
        """
        Calcula o center de um objeto com base em seus vértices

        @return (tuple[int, int]): (Cx, Cy)
        """
        n = len(points)
        cx = 0
        cy = 0
        for i in range(n):
            cx += points[i].coordenadas[0]
        for i in range(n):
            cy += points[i].coordenadas[1]
        cx = cx/n
        cy = cy/n
        return (int(cx), int(cy))
