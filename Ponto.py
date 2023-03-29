from objeto import Objeto, Tipo

class Ponto(Objeto):
    def __init__(self, nome: str, coordenadas: tuple[int, int]) -> None:
        if len(coordenadas) != 2:
            raise Exception('Para criar um ponto são necessárias duas, e apenas duas, coordenadas.')
        super().__init__(nome, Tipo.PONTO)
        self.coordenadas = coordenadas

    def translate(self, dx: int, dy: int) -> tuple[int, int]:
        self.coordenadas = super().translate(self.coordenadas, dx, dy)
    
    def rotate(self, angle, center) -> tuple[int, int]:
        cx, cy = center
        self.translate(-cx, -cy)
        self.coordenadas = super().rotate(self.coordenadas, angle)
        self.translate(cx, cy)
