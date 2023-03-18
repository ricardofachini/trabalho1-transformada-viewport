import sys
from PyQt6 import uic, QtWidgets


class Dialog(QtWidgets.QDialog):
    """
    Janela de configuração para a criação de objetos
    """
    def __init__(self, *args, **kwargs):
        super(Dialog, self).__init__(*args, **kwargs)
        self.setWindowTitle("Configurações")
        uic.loadUi("UI/AddPolygon.ui", self)

        self.okPointButton.clicked.connect(self.insert_point)
        self.okLineButton.clicked.connect(self.insert_line)
        self.okPolygonButton.clicked.connect(self.insert_polygon)
    
    def insert_point(self):
        nome = self.lineEdit.text()
        x = int(self.posXPoint.text())
        y = int(self.posYPoint.text())
        print(f"ponto inserido: {nome}, coordenadas: {(x, y)}") #temporario
    
    def insert_line(self):
        nome = self.lineEdit.text()
        print(f"reta inserida: {nome}")

    def insert_polygon(self):
        nome = self.lineEdit.text()
        print(f"poligono inserido: {nome}")
