from PyQt6 import QtWidgets, uic
from objeto import Objeto


class TransformDialog(QtWidgets.QDialog):

    def __init__(self, objeto: Objeto, *args, **kwargs) -> None:
        super(TransformDialog, self).__init__(*args, **kwargs)
        self.objeto = objeto
        uic.loadUi("UI/Transform.ui", self)
        self.setWindowTitle(f"Transformar {objeto.nome}")

        self.okButton.clicked.connect(self.add_transformation)

    def add_transformation(self):
        self.objeto.zoom(1.2)
        self.close()
