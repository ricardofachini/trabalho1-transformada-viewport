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
        uic.loadUi("UI/AddObject.ui", self)
        self.setWindowTitle("Adicionar objeto")
        self.line_color = "#000000"

        self.inserted_type = None

        self.okPointButton.clicked.connect(self.insert_point)
        self.okLineButton.clicked.connect(self.insert_line)
        self.okPolygonButton.clicked.connect(self.insert_polygon)
        self.pickColor.clicked.connect(self.choose_color_dialog)
    
    def insert_point(self):
        nome = self.lineEdit.text()
        if not nome:
            self.missing_name_popup()
        else:
            x = (int) (self.posXPoint.text())
            y = (int) (self.posYPoint.text())
            self.inserted_type = Tipo.PONTO
            self.object = Ponto(nome, (x, y))
            self.close()
    
    def insert_line(self):
        nome = self.lineEdit.text()
        if not nome:
            self.missing_name_popup()
        else:
            self.inserted_type = Tipo.SEGMENTO_RETA

            p1 = Ponto(nome, ((int) (self.spinBoxX1Line.text()), (int) (self.spinBoxY1Line.text())))
            p2 = Ponto(nome, ((int) (self.spinBoxX2Line.text()), (int) (self.spinBoxY2Line.text())))
            self.object = Reta(nome, (p1, p2), self.line_color)
            
            self.close()

    def insert_polygon(self):
        nome = self.lineEdit.text()
        if not nome:
            self.missing_name_popup()
        else:
            self.inserted_type = Tipo.POLIGONO
            centro = Ponto('', ((int) (self.spinBoxXPolyCen.text()), (int) (self.spinBoxYPolyCen.text())))
            n_linhas = (int) (self.spinBoxBordersQtd.text())
            tam_linhas = (int) (self.spinBoxLinesSize.text())
            self.object = WireFrame(nome, centro, n_linhas, tam_linhas)
            self.close()
    
    def missing_name_popup(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle('Campo Nome Obrigatório')
        msg.setText('Preencha o campo nome para referenciar o objeto criado')
        msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msg.exec()

    def choose_color_dialog(self):
        color_dialog = QtWidgets.QColorDialog()
        color_dialog.show()
        color_dialog.exec()

        selected_color = color_dialog.selectedColor()
        self.line_color = selected_color.name()
