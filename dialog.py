import sys
from PyQt6 import uic, QtWidgets


class Dialog(QtWidgets.QDialog):
    """
    Janela de configuração para a criação de objetos
    """
    def __init__(self, *args, **kwargs):
        super(Dialog, self).__init__(*args, **kwargs)
        self.setWindowTitle("Configurações")
        uic.loadUi("AddObject.ui", self)
