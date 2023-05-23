import numpy as np

from src.objeto import Objeto, Tipo
from src.Wireframe import WireFrame
from src.constants import C_MATRIX, M_BS


class Curva2D(Objeto):

    def __init__(self, nome: str, pontos_iniciais, pontos: list = []):
        super().__init__(nome, Tipo.CURVA)
        self.pontos_iniciais = pontos_iniciais  # lista de tuplas

        # Coordenadas da letra M
        # (-120, 0), (-100, 50), (-80, 100), (-60, 150), (-40, 100), (-20, 50), (0, 0), 
        # (20, 50), (40, 100), (60, 150), (80, 100), (100, 50), (120, 0)

        if len(pontos) == 0:
            if len(pontos_iniciais) > 4:
                segments = self.get_segments(pontos_iniciais)
                for i in range(len(segments)):
                    # print(f'{segment = }')
                    result = self.bspline(segments[i])
                    if i > 0:
                        prev = pontos[-1]
                        curr = result[0]
                        print(f'{prev = }, {curr = }')
                        diff_x, diff_y = curr[0] - prev[0], curr[1] - prev[1]
                        result = list(map(lambda x: (x[0] - diff_x, x[1] - diff_y), result))
                    
                    # print(f'{result = }')
                    pontos += result
            else:
                pontos = self.cubic_bezier_curve()
        self.pontos = pontos
        # print(f'{pontos = }')
        self.poligono = WireFrame(nome, (0, 0), len(self.pontos)-1, 0, pontos=self.pontos)

    def get_segments(self, points):
        segments = []
        aux = []
        n = 0
        size = len(points)
        for i in range(size + (size // 4)):
            if (i % 4) == 0 and (i > 0):
                segments.append(aux)
                aux = []
                n += 1

            aux.append(points[i - n])

        if aux:
            segments.append(aux)
        
        return segments

    def bezier_blending_function(self, t: float) -> np.array:
        """
        Retorna o resultado da multiplicação da matriz Mb pelo vetor T: [t³ t² t 1],
        expresso em um vetor de quatro valores
        t: int = Valor do passo de iteração
        """
        t2 = t * t
        t3 = t2 * t
        t_matrix = np.array([1, t, t2, t3])
        return t_matrix @ C_MATRIX

    def cubic_bezier_curve(self, k=50):
        """
        Calcula os pontos da curva bezier, com k o fator de aproximação:
        um k maior significa uma curva mais precisa. Quanto menor o k, mais proximo de um poligono a curva está
        """
        # x e y dos pontos iniciais, cada p é uma tupla
        p0 = self.pontos_iniciais[0]
        p1 = self.pontos_iniciais[1]
        p2 = self.pontos_iniciais[2]
        p3 = self.pontos_iniciais[3]
        t = step = 1/k
        pontos = []
        for _ in range(k):
            ponto_atual = self.bezier_blending_function(t) @ np.array([p0, p1, p2, p3])
            pontos.append(ponto_atual)
            t += step
        return pontos

    def bspline(self, pontos, d=0.005):
        d2 = d * d
        d3 = d2 * d
        E = np.array([[   0,    0, 0, 1],
                      [  d3,   d2, d, 0],
                      [6*d3, 2*d2, 0, 0],
                      [6*d3,    0, 0, 0]])

        Gx = np.array([])
        Gy = np.array([])

        for ponto in pontos:
            Gx = np.append(Gx, ponto[0])
            Gy = np.append(Gy, ponto[1])
        
        Cx = M_BS @ Gx
        Cy = M_BS @ Gy

        Fx = E @ Cx
        Fy = E @ Cy

        return self.forward_differences(int(1/d), Fx, Fy)
    
    def forward_differences(self, n, Fx, Fy):
        pontos = []

        i = 0
        x_velho, dx, d2x, d3x = Fx
        y_velho, dy, d2y, d3y = Fy
        while i < n:
            i += 1
            
            x = x_velho + dx
            dx = dx + d2x
            d2x = d2x + d3x

            y = y_velho + dy
            dy = dy + d2y
            d2y = d2y + d3y

            x_velho, y_velho = x, y

            pontos.append((int(x), int(y)))
        
        return pontos

    def zoom(self, scale):
        self.poligono.zoom(scale)

    def translate(self, dx: int, dy: int):
        self.poligono.translate(dx, dy)

    def rotate(self, rotation_side, center):
        self.poligono.rotate(rotation_side, center)

    def draw(self, canvas, container, get_vp_coords, world_coords):
        self.poligono.draw(canvas, container, get_vp_coords, world_coords)
