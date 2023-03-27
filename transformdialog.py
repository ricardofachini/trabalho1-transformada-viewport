from PyQt6 import QtWidgets, uic
from objeto import Objeto


class TransformDialog(QtWidgets.QDialog):
    """
    Classe para o dialog que permite transformar algum objeto ja renderizado na viewport
    """

    def __init__(self, objeto: Objeto, *args, **kwargs) -> None:
        super(TransformDialog, self).__init__(*args, **kwargs)
        self.objeto = objeto
        uic.loadUi("UI/Transform.ui", self)
        self.setWindowTitle(f"Transformar {objeto.nome}")

        self.okTranslateButton.clicked.connect(self.translate_transform)
        self.okScaleButton.clicked.connect(self.scale_transform)
        self.okRotateButton.clicked.connect(self.rotate_transform)

    def translate_transform(self):
        self.objeto.translate("", 20, 20) #arrumar
        self.close()

    def scale_transform(self):
        self.objeto.zoom(1.2)
        self.close()

    def rotate_transform(self):
        #self.objeto.rotate()
        self.close()
