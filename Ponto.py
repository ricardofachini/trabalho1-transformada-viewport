from objeto import Objeto, Tipo

class Ponto(Objeto):
    def __init__(self, nome: str, coordenadas: list[tuple[float]]) -> None:
        if len(coordenadas) != 2:
            raise Exception('Para criar um ponto são necessárias doas, e apenas doas, coordenadas.')
        super().__init__(nome, Tipo.PONTO)
        self.coordenadas = coordenadas
