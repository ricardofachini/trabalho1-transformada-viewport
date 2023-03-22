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
    def __init__(self, nome: str, tipo: Tipo) -> None:
        self.nome = nome
        self.tipo = tipo
        #self.centro = self.calculate_center()

    def rotate(self, points: list, angle) -> tuple[int, int]:
        """
        Recebe uma tupla de coordenadas 2D, e retorna a tupla rotacionada
        """
        rad = radians(angle)
        # transformation_matrix = [[cos(rad), -sin(rad), 0], 
        #                          [sin(rad), cos(rad) , 0], 
        #                          [0       , 0        , 1]]
        current_vector = [points[0], points[1]]
        # x = 0
        # y = 0
        # for i in range(3):
        #     x += current_vector[0]*transformation_matrix[0][i]
        # for i in range(3):
        #     y += current_vector[1]*transformation_matrix[1][i]

        x = current_vector[0] * cos(rad) - current_vector[1] * sin(rad)
        y = current_vector[0] * sin(rad) + current_vector[1] * cos(rad)
        return (x, y)
    
    def scale(self, points: tuple, sx, sy) -> tuple[int, int]:
        """
        Recebe uma tupla de coordenadas 2D, e retorna a tupla escalonada
        """
        transformation_matrix = [[sx, 0, 0], [0, sy, 0], [0, 0, 1]]
        current_vector = [points[0], points[1]]
        x = 0
        y = 0
        for i in range(3):
            x += current_vector[0]*transformation_matrix[0][i]
        for i in range(3):
            y += current_vector[1]*transformation_matrix[1][i]
        return ((int) (x), (int) (y))
    
    def translate(self, points: tuple, dx, dy) -> tuple[int, int]:
        """
        Recebe uma tupla de coordenadas 2D, e retorna a tupla translada
        """
        return(points[0] + dx, points[1] + dy)

    # def calculate_center(self) -> tuple[int, int]:
    #     """
    #     Calcula o centro de um objeto com base em seus vértices

    #     @return (tuple[int, int]): (Cx, Cy)
    #     """
    #     n = len(self.pontos)
    #     cx = 0
    #     cy = 0
    #     for i in range(n):
    #         cx += self.pontos[i].coordenadas[0]
    #     for i in range(n):
    #         cy += self.pontos[i].coordenadas[1]
    #     cx = cx/n
    #     cy = cy/n
    #     return (int(cx), int(cy))
