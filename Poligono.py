from objeto import Objeto, Tipo
from Reta import Reta

class Poligono(Objeto):
    def __init__(self, nome: str, pontos: list[tuple[Reta]]) -> None:
        if len(pontos) < 3:
            raise Exception('Para criar um poligono são necessárias pelo menos três pontos interligados.')
        super().__init__(nome, Tipo.POLIGONO)
        self.pontos = pontos
