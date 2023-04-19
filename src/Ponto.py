from src.objeto import Objeto, Tipo
from src.Vertice import Vertice


class Ponto(Objeto):
    def __init__(self, nome: str, coordenadas: Vertice) -> None:
        if len(coordenadas.world_coordinates) != 2:
            raise Exception('Para criar um ponto são necessárias duas, e apenas duas, coordenadas.')
        super().__init__(nome, Tipo.PONTO)
        self.coordenadas = coordenadas

    def translate(self, dx: int, dy: int) -> tuple[int, int]:
        self.coordenadas.world_coordinates = super().translate(self.coordenadas.world_coordinates, dx, dy)
    
    def rotate(self, angle, center) -> tuple[int, int]:
        cx, cy = center
        self.translate(-cx, -cy)
        self.coordenadas.world_coordinates = super().rotate(self.coordenadas.world_coordinates, angle)
        self.translate(cx, cy)
    
    def should_draw(self, xmin, xmax, ymin, ymax, xw, yw):
        return ((xw > xmin) and (xw < xmax)) and ((yw > ymin) and (yw < ymax))
