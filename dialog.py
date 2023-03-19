import sys
from PyQt6 import uic, QtWidgets
from objeto import Tipo

from Ponto import Ponto
from Reta import Reta
from Poligono import WireFrame


class Dialog(QtWidgets.QDialog):
    """
    Janela de configuração para a criação de objetos
    """
    def __init__(self, *args, **kwargs):
        super(Dialog, self).__init__(*args, **kwargs)
        self.setWindowTitle("Configurações")
        uic.loadUi("UI/AddObject.ui", self)

        self.inserted_type = None

        self.okPointButton.clicked.connect(self.insert_point)
        self.okLineButton.clicked.connect(self.insert_line)
        self.okPolygonButton.clicked.connect(self.insert_polygon)
    
    def insert_point(self):
        nome = self.lineEdit.text()
        x = int(self.posXPoint.text())
        y = int(self.posYPoint.text())
        self.inserted_type = Tipo.PONTO
        self.close()
    
    def insert_line(self):
        nome = self.lineEdit.text()
        self.inserted_type = Tipo.SEGMENTO_RETA

        p1 = Ponto(nome, (int(self.spinBoxX1Line.text()), int(self.spinBoxY1Line.text())))
        p2 = Ponto(nome, (int(self.spinBoxX2Line.text()), int(self.spinBoxY2Line.text())))
        self.object = Reta(nome, (p1, p2))
        
        self.close()

    def insert_polygon(self):
        nome = self.lineEdit.text()
        self.inserted_type = Tipo.POLIGONO
        self.close()
