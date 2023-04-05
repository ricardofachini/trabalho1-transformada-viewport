from src.objeto import Tipo

VERTICE_PREFIX = "v "
POINT_PREFIX = "p "
OBJECT_PREFIX = "o "
LINE_PREFIX = "l "
LINE_BREAK = "\n"


class ObjDescriptor:
    """
    Classe que importa e exporta arquivos Wavefront e
    realiza as transformações de .obj para
    coordenadas do sistema e vice-versa
    """
    def __init__(self) -> None:
        self.wavefront_string: str = ""

    def export_file(self, path: str):
        """
        Exporta um arquivo Wavefront OBJ com a extensão .obj de todos os objetos
        """
        path = path[0].replace(".obj", "")
        with open(f"{path}.obj", 'w+') as file:
            string = f"mtllib {path[-1]}.mtl\n\n"
            string += self.wavefront_string
            file.write(string)
        self.wavefront_string = ""
        with open(f"{path}.mtl", 'w+') as material_file:
            material_file.write("newmtl red\nKd 1.000000 0.000000 0.000000\nnewmtl texture\nKd 0.800000 0.800000 0.800000")

    def transform_to_wavefront(self, item):
        """
        Transforma coordenadas de um objeto para uma string no formato wavefront
        """
        string = OBJECT_PREFIX + item.nome + LINE_BREAK
        if item.tipo is Tipo.SEGMENTO_RETA:
            '''
            Caso o objeto seja uma reta
            '''
            for vertice in item.pontos:
                coordenadas = tuple(float(number) for number in vertice.coordenadas)
                string += VERTICE_PREFIX + str(coordenadas).replace("(", "") + " 0.0" + LINE_BREAK
            contagem = len(item.pontos)
            string += LINE_PREFIX
            for i in range(contagem):
                string += f"{-(contagem - i)} "

        elif item.tipo is Tipo.POLIGONO:
            for vertice in item.points:
                coordenadas = tuple(float(number) for number in vertice)
                string += VERTICE_PREFIX + str(coordenadas).replace("(", "") + " 0.0" + LINE_BREAK
            contagem = len(item.points)
            string += LINE_PREFIX
            for i in range(contagem):
                string += f"{-(contagem - i)} "

        elif item is Tipo.PONTO:
            coordenadas = tuple(float(number) for number in item.coordenadas)
            string += VERTICE_PREFIX + str(coordenadas).replace("(", "") + " 0.0" + LINE_BREAK
            contagem = len(item.coordenadas)
            string += POINT_PREFIX
            for i in range(contagem):
                string += f"{-(contagem - i)} "

        string += "\nusemtl red"
        string=string.replace(")", "")
        string=string.replace(",", "")
        string += LINE_BREAK

        self.wavefront_string += string
