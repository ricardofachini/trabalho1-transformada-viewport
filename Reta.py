from objeto import Objeto, Tipo
from Ponto import Ponto

class Reta(Objeto):
    def __init__(self, nome: str, pontos: list[tuple[Ponto]]) -> None:
        if len(pontos) != 2:
            raise Exception('Para criar uma reta são necessários dois, e apenas dois, pontos.')
        super().__init__(nome, Tipo.SEGMENTO_RETA)
        self.pontos = pontos
