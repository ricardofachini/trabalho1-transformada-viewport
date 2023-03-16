# This Python file uses the following encoding: utf-8
import sys
from PyQt6 import uic, QtWidgets
from objeto import Tipo


class MainWindow(QtWidgets.QMainWindow):
    """
    Janela principal do qt que possui os widgets
    """
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Trabalho 1 - Computação gráfica")
        uic.loadUi("MainWindow - untitled.ui", self)

        self.listOfCurrentObjects.setObjectName("listView")
        self.listOfCurrentObjects.addItems(["One", "two"])
        self.comboBoxOfTypes.addItems([Tipo.POLIGONO.value, Tipo.PONTO.value])



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
