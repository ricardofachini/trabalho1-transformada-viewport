class Vertice:

    def __init__(self, *coordinates):
        self.world_coordinates = coordinates
        self.cpp_coordinates = tuple()
