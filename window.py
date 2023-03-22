from math import sin, cos, radians

class Window:
    """
    Classe para a Window de coordenadas de mundo
    """
    def __init__(self) -> None:
        self.minXwp = 0
        self.minYwp = 0
        self.maxXwp = 1000
        self.maxYwp = 1000
        self.width = self.maxXwp - self.minXwp
        self.height = self.maxYwp - self.minYwp
        self.centerX = self.minXwp + (self.width / 2)
        self.centerY = self.minYwp + (self.height / 2)

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

    '''def translate(self, points: tuple, dx, dy) -> tuple[int, int]:
        """
        Recebe uma tupla de coordenadas 2D, e retorna a tupla translada
        """
        return(points[0] + dx, points[1] + dy)

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
        return (x, y)'''
