from math import sin, cos

class WindowTransformation:
    def __init__(self) -> None:
        pass

    def translate(self, points: tuple, dx, dy) -> tuple[int, int]:
        """
        Recebe uma tupla de coordenadas 2D, e retorna a tupla translada
        """
        transformation_matrix = [[1, 0, 0], [0, 1, 0], [dx, dy, 1]]
        current_vector = [points[0], points[1], 1]
        x = 0
        y = 0
        for i in range(3):
            x += current_vector[i]*transformation_matrix[i][0]
        for i in range(3):
            y += current_vector[i]*transformation_matrix[i][1]
        print("translate:",(x, y))
        return (int(x), int(y))

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
        return (int(x), int(y))

    def rotate(self, points: list, angle) -> tuple[int, int]:
        """
        Recebe uma tupla de coordenadas 2D, e retorna a tupla rotacionada
        """
        transformation_matrix = [[cos(angle), -sin(angle), 0], 
                                 [sin(angle), cos(angle), 0], 
                                 [0, 0, 1]]
        current_vector = [points[0], points[1], 1]
        x = 0
        y = 0
        for i in range(3):
            x += current_vector[i]*transformation_matrix[i][0]
        for i in range(3):
            y += current_vector[i]*transformation_matrix[i][1]
        return (int(x), int(y))
