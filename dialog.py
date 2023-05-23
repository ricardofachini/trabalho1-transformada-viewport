from PyQt6 import uic, QtWidgets
from src.objeto import Tipo
from src.Vertice import Vertice
from src.Ponto import Ponto
from src.Reta import Reta
from src.Wireframe import WireFrame
from src.Curva2D import Curva2D


class Dialog(QtWidgets.QDialog):
    """
    Janela de configuração para a criação de objetos
    """
    def __init__(self, *args, **kwargs):
        super(Dialog, self).__init__(*args, **kwargs)
        uic.loadUi("UI/AddObject.ui", self)
        self.setWindowTitle("Adicionar objeto")
        self.color = "#000000"

        self.inserted_type = None

        self.okPointButton.clicked.connect(self.insert_point)
        self.okLineButton.clicked.connect(self.insert_line)
        self.okPolygonButton.clicked.connect(self.insert_polygon)
        self.okCurveButton.clicked.connect(self.insert_curve)
        self.pickColor.clicked.connect(self.choose_color_dialog)
    
    def insert_point(self):
        nome = self.lineEdit.text()
        if not nome:
            self.missing_name_popup()
        else:
            x = (int) (self.posXPoint.text())
            y = (int) (self.posYPoint.text())
            self.inserted_type = Tipo.PONTO
            self.object = Ponto(nome, Vertice(x, y))
            self.object.cor = self.color
            self.close()
    
    def insert_line(self):
        nome = self.lineEdit.text()
        if not nome:
            self.missing_name_popup()
        else:
            self.inserted_type = Tipo.SEGMENTO_RETA

            p1 = Vertice((int) (self.spinBoxX1Line.text()), (int) (self.spinBoxY1Line.text()))
            p2 = Vertice((int) (self.spinBoxX2Line.text()), (int) (self.spinBoxY2Line.text()))
            self.object = Reta(nome, (p1, p2), self.color)
            
            self.close()

    def insert_polygon(self):
        nome = self.lineEdit.text()
        if not nome:
            self.missing_name_popup()
        else:
            self.inserted_type = Tipo.POLIGONO
            center = ((int) (self.spinBoxXPolyCen.text()), (int) (self.spinBoxYPolyCen.text()))
            n_linhas = (int) (self.spinBoxBordersQtd.text())
            tam_linhas = (int) (self.spinBoxLinesSize.text())
            self.object = WireFrame(nome, center, n_linhas, tam_linhas, self.color)
            self.close()

    def insert_curve(self):
        nome = self.lineEdit.text()
        if not nome:
            self.missing_name_popup()
        else:
            self.inserted_type = Tipo.CURVA
            points = self.curvePointsTextEdit.toPlainText().strip()
            points = points.split("),")
            points = [tuple(float(x.strip()) for x in tupl.replace("(", "").replace(")", "").split(",")) for tupl in points]
            self.object = Curva2D(nome, pontos_iniciais=points)
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
        self.color = selected_color.name()
