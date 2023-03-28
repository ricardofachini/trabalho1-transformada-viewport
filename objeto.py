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
        #self.center = self.calculate_center()

    def rotate(self, coordenadas: tuple, angle) -> tuple[int, int]:
        """
        Recebe uma tupla de coordenadas 2D, e retorna a tupla rotacionada
        """
        rad = radians(angle)
        # transformation_matrix = [[cos(rad), -sin(rad), 0], 
        #                          [sin(rad), cos(rad) , 0], 
        #                          [0       , 0        , 1]]
        # current_vector = [coordenadas[0], coordenadas[1]]
        # x = 0
        # y = 0
        # for i in range(3):
        #     x += current_vector[0]*transformation_matrix[0][i]
        # for i in range(3):
        #     y += current_vector[1]*transformation_matrix[1][i]

        # print(f'{coordenadas[0] = }')
        # print(f'{cos(rad) = }')
        # print(f'{coordenadas[1] = }')
        # print(f'{sin(rad) = }')
        # print(f'{rad = }')
        
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
        return(points[0] + dx, points[1] + dy)

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
