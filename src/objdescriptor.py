from src.objeto import Tipo, Objeto
from src.Poligono import WireFrame
from src.Reta import Reta
from src.Ponto import Ponto

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

    def import_file(self, path: str) -> list[Objeto]:
        """
        Importa um arquivo Wavefront (*.obj) e converte seus objetos em objetos no display_file
        @params:
            path: (str) -> caminho e nome do arquivo a ser lido
        """
        vertices_list = []
        objects_list = []
        current_object_name = ""
        with open(path[0], "r") as file:
            for line in file:
                match line[0]:
                    case "v":
                        points = line.split(" ")
                        vertice = (float (points[1]), float(points[2]))
                        vertices_list.append(vertice)
                    case"o":
                        name = line.strip().split(" ")
                        current_object_name = name[1]
                    case "l":
                        indices_de_vertices = line.strip().split(" ")
                        if len(indices_de_vertices) > 3: #se true, é um poligono
                            #poligono = WireFrame(current_object_name, (0, 0), len(indexes)-1, 0)
                            #objects_list.append(poligono)
                            pass
                        else:
                            reta = Reta(
                                    current_object_name,
                                    (
                                        Ponto("", (
                                            vertices_list[int(indices_de_vertices[1])][0],
                                            vertices_list[(int) (indices_de_vertices[1])][1])),
                                        Ponto("", (
                                            vertices_list[(int) (indices_de_vertices[2])][0],
                                            vertices_list[(int) (indices_de_vertices[2])][1]))
                                    )
                                )
                            objects_list.append(reta)
                    case "p":
                        indice_coordenada = line.strip().split(" ")
                        ponto = Ponto(
                                    current_object_name,
                                    (
                                        vertices_list[(int) (indice_coordenada[1])][0],
                                        vertices_list[(int) (indice_coordenada[1])][1]
                                    )
                                )
                        objects_list.append(ponto)
        return objects_list

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
            for retas in item.retas:
                for vertice in retas.pontos:
                    coordenadas = tuple(float(number) for number in vertice.coordenadas)
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
