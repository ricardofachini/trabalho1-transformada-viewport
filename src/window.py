from src.constants import ROTATION_LEFT, ROTATION_RIGHT
from src.objeto import RotateSide

import numpy as np

class Window:
    """
    Classe para a Window de coordenadas de mundo
    """
    def __init__(self) -> None:
        self.minXwp  = 0
        self.minYwp  = 0
        self.maxXwp  = 1000
        self.maxYwp  = 1000
        self.width   = self.maxXwp - self.minXwp
        self.height  = self.maxYwp - self.minYwp
        self.centerX = self.minXwp + (self.width / 2)
        self.centerY = self.minYwp + (self.height / 2)
        self.center  = (self.centerX, self.centerY)

    def scale(self, scale_value):
        self.minXwp //= scale_value
        self.minYwp //= scale_value
        self.maxXwp //= scale_value
        self.maxYwp //= scale_value

    def translate(self, dx, dy):
        self.minXwp += dx
        self.maxXwp += dx
        self.minYwp += dy
        self.maxYwp += dy
    
    def rotate(self, rotation_side):
        rot_matrix = ROTATION_LEFT if rotation_side == RotateSide.LEFT else ROTATION_RIGHT
        
        # atualiza posição da window
        result_matrix  = np.array([self.minXwp, self.maxXwp, 1]) @ rot_matrix
        self.minXwp, self.maxXwp = result_matrix[0], result_matrix[1]

        result_matrix  = np.array([self.minYwp, self.maxYwp, 1]) @ rot_matrix
        self.minYwp, self.maxYwp = result_matrix[0], result_matrix[1]

    #transformadas de viewport
    def get_x_to_viewport(self, x_window, vp_width):
        return ((x_window - self.minXwp) / (self.maxXwp - self.minXwp)) * vp_width

    def get_y_to_viewport(self, y_window, vp_height):
        return (1 - ((y_window - self.minYwp) / (self.maxYwp - self.minYwp))) * vp_height
