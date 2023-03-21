from windowtransformation import WindowTransformation


class ViewPortTransform:

    def __init__(self) -> None:
        self.minXvp = 0
        self.minYvp = 0
        self.maxXvp = 531
        self.maxYvp = 511
        self.window = WindowTransformation()

    def get_x_viewport(self, x_window):
        return ((x_window - self.window.minXwp) / (self.window.maxXwp - self.window.minXwp)) * (self.maxXvp - self.minXvp)
    
    def get_y_viewport(self, y_window):
        return (1 - ((y_window - self.window.minYwp) / (self.window.maxYwp - self.window.minYwp))) * (self.maxYvp - self.minYvp)