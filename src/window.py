from src.constants import ROTATION_LEFT, ROTATION_RIGHT
from src.objeto import RotateSide

import numpy as np

class Window:
    """
    Classe para a Window de coordenadas de mundo
    """
    def __init__(self) -> None:
        self.minX  = -500
        self.minY  = -500
        self.maxX  = 500
        self.maxY  = 500
        self.width   = self.maxX - self.minX
        self.height  = self.maxY - self.minY
        self.centerX = self.minX + (self.width / 2)
        self.centerY = self.minY + (self.height / 2)
        self.center  = (self.centerX, self.centerY)

    def scale(self, scale_value):
        self.minX //= scale_value
        self.minY //= scale_value
        self.maxX //= scale_value
        self.maxY //= scale_value

    def translate(self, dx, dy):
        self.minX    += dx
        self.maxX    += dx
        self.centerX += dx
        
        self.minY    += dy
        self.maxY    += dy
        self.centerY += dy

        self.center = (self.centerX, self.centerY)
    
    def rotate(self, rotation_side):
        # rot_matrix = ROTATION_LEFT if rotation_side == RotateSide.LEFT else ROTATION_RIGHT

        # result_matrix  = np.array([self.minX, self.maxX, 1]) @ rot_matrix
        # self.minX, self.maxX = result_matrix[0], result_matrix[1]

        # result_matrix  = np.array([self.minY, self.maxY, 1]) @ rot_matrix
        # self.minY, self.maxY = result_matrix[0], result_matrix[1]

        # print(f'Rotacionou')
        # print(f'{self.minX, self.maxX = }')
        # print(f'{self.minY, self.maxY = }')
        # print()
        pass

    #transformadas de viewport
    def get_x_to_viewport(self, x_window, vp_width):
        return ((x_window - self.minX) / (self.maxX - self.minX)) * vp_width

    def get_y_to_viewport(self, y_window, vp_height):
        return (1 - ((y_window - self.minY) / (self.maxY - self.minY))) * vp_height
