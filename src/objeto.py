from enum import Enum
import numpy as np
from math import sin, cos, radians

from src.constants import ROTATION_LEFT, ROTATION_RIGHT

class Tipo(Enum):
    """
    os tipos de objetos que o sistema suporta
    """
    PONTO = "PONTO"
    SEGMENTO_RETA = "RETA"
    POLIGONO = "POLIGONO"


class RotateSide(Enum):
    LEFT  = 0
    RIGHT = 1


class Objeto:
    """
    Classe genérica para um objeto qualquer
    """
    def __init__(self, nome: str, tipo: Tipo, cor: str = "#000000") -> None:
        self.nome = nome
        self.tipo = tipo
        self.cor = cor

    def rotate(self, coordenadas, center, rotation_side, angle=None) -> tuple[int, int]:
        """
        Recebe uma tupla de coordenadas 2D, e retorna a tupla rotacionada
        """
        if angle is not None:
            rad = radians(angle)
            rot_matrix = np.array([[cos(rad), -sin(rad), 0], [sin(rad), cos(rad), 0], [0, 0, 1]])
        else:
            rot_matrix = ROTATION_LEFT if rotation_side == RotateSide.LEFT else ROTATION_RIGHT
        
        to_window_center = np.array([[1, 0, 0], [0, 1, 0], [-center[0], -center[1], 1]])
        to_own_center    = np.array([[1, 0, 0], [0, 1, 0], [center[0], center[1], 1]])  
        
        current_vector = np.array([coordenadas[0], coordenadas[1], 1])

        result_matrix  = current_vector @ (to_window_center @ rot_matrix @ to_own_center)

        return (result_matrix[0], result_matrix[1])
    
    def scale(self, points: tuple, scale, center) -> tuple[int, int]:
        """
        Recebe uma tupla de coordenadas 2D, e retorna a tupla escalonada
        """
        sx = sy = scale
        transformation_matrix = np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])
        
        to_window_center      = np.array([[1, 0, 0], [0, 1, 0], [-center[0], -center[1], 1]])
        to_own_center         = np.array([[1, 0, 0], [0, 1, 0], [center[0], center[1], 1]])
        
        current_vector        = np.array([points[0], points[1], 1])
        
        result_matrix         = current_vector @ (to_window_center @ transformation_matrix @ to_own_center)
        
        return (result_matrix[0], result_matrix[1])
    
    def translate(self, coordenadas: tuple, dx: int, dy: int) -> tuple[int, int]:
        """
        Recebe uma tupla de coordenadas 2D, e retorna a tupla translada
        """
        coordenadas        = np.array([coordenadas[0], coordenadas[1], 1])
        translation_matrix = np.array([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])

        result_matrix = coordenadas @ translation_matrix          
        
        return (result_matrix[0], result_matrix[1])

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
