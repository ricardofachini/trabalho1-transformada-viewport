from src.objeto import Objeto, Tipo
from src.Wireframe import WireFrame


class Curva2D(Objeto):

    def __init__(self, nome: str, pontos_iniciais, pontos: [] = None):
        super().__init__(nome, Tipo.CURVA)
        self.pontos_iniciais = pontos_iniciais  # lista de tuplas

        if pontos is None:
            pontos = self.cubic_bezier_curve()
        self.pontos = pontos
        self.poligono = WireFrame(nome, (0, 0), len(self.pontos)-1, 0, pontos=self.pontos)

    def bezier_blending_function(self, t: float) -> list:
        """
        Retorna o resultado da multiplicação da matriz Mb pelo vetor T: [t³ t² t 1],
        expresso em um vetor de quatro valores
        t: int = Valor do passo de iteração
        """
        return [-t**3 + 3*(t**2) - 3*t + 1, 3*(t**3) - 6*(t**2) + 3*t, -3*(t**3) + 3*(t**2), t**3]

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
        t = 1/k
        pontos = []
        for i in range(k):
            blend_func = self.bezier_blending_function(t)  # calcula a função de aproximação para cada passo k
            # calcula o x do ponto
            x = p0[0] * blend_func[0] + p1[0] * blend_func[1] + p2[0] * blend_func[2] + p3[0] * blend_func[3]
            # calcula o y do ponto
            y = p0[1] * blend_func[0] + p1[1] * blend_func[1] + p2[1] * blend_func[2] + p3[1] * blend_func[3]
            ponto_atual = (x, y)
            pontos.append(ponto_atual)
            t += 1/k
        return pontos

    def zoom(self, scale):
        self.poligono.zoom(scale)

    def translate(self, dx: int, dy: int):
        self.poligono.translate(dx, dy)

    def rotate(self, rotation_side, center):
        self.poligono.rotate(rotation_side, center)

    def draw(self, canvas, container, get_vp_coords, world_coords):
        self.poligono.draw(canvas, container, get_vp_coords, world_coords)
