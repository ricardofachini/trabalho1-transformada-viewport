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
        self.cpp_w1 = (self.minX, self.minY)
        self.cpp_w2 = (self.minX, self.maxY)
        self.cpp_w3 = (self.maxX, self.maxY)
        self.cpp_w4 = (self.maxX, self.minY)
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
    

    def get_view_up_angle(self):
        cat_oposto = int(abs(self.cpp_w1[0] - self.cpp_w2[0]))
        cat_adjacente = int(abs(self.cpp_w2[1] - self.cpp_w1[1]))
        angle = np.arctan(cat_oposto / cat_adjacente)
        return angle

    def gen_cpp_description(self):
        self.translate(-self.centerX, -self.centerY)

        #v_up = (self.cpp_w1, self.cpp_w2)
        view_up_angle = self.get_view_up_angle()
        if view_up_angle != 0:
            print("ORIENTAÇÃO ROTACIONADA")

    def rotate(self, rotation_side):
        rot_matrix = ROTATION_LEFT if rotation_side == RotateSide.LEFT else ROTATION_RIGHT

        #calcula a rotação nos 4 pontos da window
        result_matrix  = np.array([self.cpp_w1[0], self.cpp_w1[1], 1]) @ rot_matrix
        self.cpp_w1 = result_matrix[0], result_matrix[1]

        result_matrix  = np.array([self.cpp_w2[0], self.cpp_w2[1], 1]) @ rot_matrix
        self.cpp_w2 = result_matrix[0], result_matrix[1]

        result_matrix  = np.array([self.cpp_w3[0], self.cpp_w3[1], 1]) @ rot_matrix
        self.cpp_w3 = result_matrix[0], result_matrix[1]

        result_matrix  = np.array([self.cpp_w4[0], self.cpp_w4[1], 1]) @ rot_matrix
        self.cpp_w4 = result_matrix[0], result_matrix[1]

        #result_matrix  = np.array([self.minY, self.maxY, 1]) @ rot_matrix
        #self.minY, self.maxY = result_matrix[0], result_matrix[1]

        self.gen_cpp_description()

        print(f'Rotacionou')
        print(f'{self.cpp_w1, self.cpp_w2 = }')
        print(f'{self.cpp_w3, self.cpp_w4 = }')
        print()
        pass

    #transformadas de viewport
    def get_x_to_viewport(self, x_window, vp_width):
        """Retorna o x de uma coordenada transformado ao sistema
        de coordenadas da Viewport
        @params: 
            x_window = x na coordenada de mundo
            vp_width = largura da viewport
        """
        return ((x_window - self.minX) / (self.maxX - self.minX)) * vp_width

    def get_y_to_viewport(self, y_window, vp_height):
        """Retorna o x de uma coordenada transformado ao sistema
        de coordenadas da Viewport
        @params: 
            y_window = y na coordenada de mundo
            vp_height = altura da viewport
        """
        return (1 - ((y_window - self.minY) / (self.maxY - self.minY))) * vp_height
