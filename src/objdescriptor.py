from src.objeto import Tipo, Objeto
from src.Wireframe import WireFrame
from src.Reta import Reta
from src.Ponto import Ponto
from src.Vertice import Vertice

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
        with open(path, "r") as file:
            for line in file:
                if line[0] == "v":
                    points = line.split(" ")
                    vertice = (float(points[1]), float(points[2]))
                    vertices_list.append(vertice)
                elif line[0] == "o":
                    name = line.strip().split(" ")
                    current_object_name = name[1]
                elif line[0] == "l":
                    indices_de_vertices = line.strip().split(" ")
                    if len(indices_de_vertices) > 3: #se true, é um poligono
                        poligono = WireFrame(current_object_name, (0, 0), len(indices_de_vertices)-2, 0,
                                                pontos=vertices_list[-(len(indices_de_vertices)-1):])
                        objects_list.append(poligono)
                    else:
                        reta = Reta(
                                current_object_name,
                                (
                                    Vertice(
                                        vertices_list[int(indices_de_vertices[1])][0],
                                        vertices_list[int(indices_de_vertices[1])][1]),
                                    Vertice(
                                        vertices_list[int(indices_de_vertices[2])][0],
                                        vertices_list[int(indices_de_vertices[2])][1])
                                )
                            )
                        objects_list.append(reta)
                elif line[0] == "p":
                    indice_coordenada = line.strip().split(" ")
                    ponto = Ponto(
                                current_object_name,
                                Vertice(
                                    vertices_list[int(indice_coordenada[1])][0],
                                    vertices_list[int(indice_coordenada[1])][1]
                                )
                            )
                    objects_list.append(ponto)
        return objects_list

    def export_file(self, path: str, name: str):
        """
        Exporta um arquivo Wavefront OBJ com a extensão .obj de todos os objetos
        """
        path = path.replace(".obj", "")
        name = name.replace(".obj", "")
        with open(f"{path}.obj", 'w+') as file:
            string = f"mtllib {name}.mtl\n\n"
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
                coordenadas = tuple(float(number) for number in vertice.world_coordinates)
                string += VERTICE_PREFIX + str(coordenadas).replace("(", "") + " 0.0" + LINE_BREAK
            contagem = len(item.pontos)
            string += LINE_PREFIX
            for i in range(contagem):
                string += f"{-(contagem - i)} "

        elif item.tipo is Tipo.POLIGONO:
            coordenada_anterior = None
            for retas in item.retas:
                for vertice in retas.pontos:
                    coordenadas = tuple(float(number) for number in vertice.world_coordinates)

                    if (str(coordenadas).replace("(", "")) != coordenada_anterior:
                        string += VERTICE_PREFIX + str(coordenadas).replace("(", "") + " 0.0" + LINE_BREAK
                        coordenada_anterior = str(coordenadas).replace("(", "")

            contagem = len(item.points)
            string += LINE_PREFIX
            for i in range(contagem):
                string += f"{-(contagem - i)} "

        elif item.tipo is Tipo.PONTO:
            coordenadas = tuple(float(number) for number in item.coordenadas.world_coordinates)
            string += VERTICE_PREFIX + str(coordenadas).replace("(", "") + " 0.0" + LINE_BREAK
            string += POINT_PREFIX
            string += "-1"

        string += "\nusemtl red"
        string = string.replace(")", "")
        string = string.replace(",", "")
        string += LINE_BREAK

        self.wavefront_string += string
