

class Window:
    """
    Classe para a Window de coordenadas de mundo
    """
    def __init__(self) -> None:
        self.minXwp = 0
        self.minYwp = 0
        self.maxXwp = 1000
        self.maxYwp = 1000
        self.width = self.maxXwp - self.minXwp
        self.height = self.maxYwp - self.minYwp
        self.centerX = self.minXwp + (self.width / 2)
        self.centerY = self.minYwp + (self.height / 2)

    def scale(self, scale_value):
        self.minXwp //= scale_value
        self.minYwp //= scale_value
        self.maxXwp //= scale_value
        self.maxYwp //= scale_value

    def translate(self, dx, dy):
        self.minXwp += dx
        self.maxXwp += dx
        self.minYwp += dy
        self.maxYwp += dy
