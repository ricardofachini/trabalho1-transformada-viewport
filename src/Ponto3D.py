from math import cos, sin


class Ponto3D:

    def __init__(self, nome: str, x: int, y: int, z: int):
        self.nome = nome
        self.x = x
        self.y = y
        self.z = z

    def rotate(self, angle, axis):
        rotation_by_x_matrix = [
            [1, 0, 0, 0], [0, cos(angle), sin(angle), 0], [0, -sin(angle), cos(angle), 0], [0, 0, 0, 1]
        ]
        rotation_by_y_matrix = [
            [cos(angle), 0, -sin(angle), 0], [0, 1, 0, 0], [sin(angle), 0, cos(angle), 0], [0, 0, 0, 1]
        ]
        rotation_by_z_matrix = [
            [cos(angle), sin(angle), 0, 0], [-sin(angle), cos(angle), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]
        ]
        if axis == "x":
            print("eixo x")
        elif axis == "y":
            print("eixo y")
        elif axis == "z":
            print("eixo z")

    def translate(self, Tx, Ty, Tz):
        self.x = self.x + Tx
        self.y = self.y + Ty
        self.z = self.z + Tz

    def scale(self, Sx, Sy, Sz):
        self.x = Sx * self.x
        self.y = Sy * self.y
        self.z = Sz * self.z
