from objeto import Objeto, Tipo
from Reta import Reta

class Poligono(Objeto):
    def __init__(self, nome: str, retas: list[tuple[Reta]]) -> None:
        if len(retas) < 3:
            raise Exception('Para criar uma reta são necessárias pelo menos três retas.')
        super().__init__(nome, Tipo.POLIGONO)
        self.retas = retas
