from math import sin, cos

class WindowTransformation:
    def __init__(self) -> None:
        pass

    def translate(self, points: list, dx, dy):
        transformation_matrix = [[1, 0, 0], [0, 1, 0], [dx, dy, 0]]

    def scale(self, points: list, sx, sy):
        transformation_matrix = [[sx, 0, 0], [sy, 0, 0], [0, 0, 1]]

    def rotate(self, points: list, angle):
        transformation_matrix = [[cos(angle), -sin(angle), 0], 
                                 [sin(angle), cos(angle), 0], 
                                 [0, 0, 1]]