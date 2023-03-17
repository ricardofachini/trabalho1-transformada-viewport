# This Python file uses the following encoding: utf-8
import sys
from PyQt6 import uic, QtWidgets
from objeto import Tipo
import images_rcc
from dialog import Dialog


class MainWindow(QtWidgets.QMainWindow):
    """
    Janela principal do qt que possui os widgets
    """
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Trabalho 1 - Computação gráfica")
        uic.loadUi("MainWindow.ui", self)

        # self.listOfCurrentObjects.setObjectName("listView")
        # self.listOfCurrentObjects.addItems(["One", "two"])
        # self.comboBoxOfTypes.addItems([Tipo.POLIGONO.value, Tipo.SEGMENTO_RETA.value, Tipo.PONTO.value])

        self.addObjectButton.clicked.connect(self.show_dialog)

    def show_dialog(self):
        dialog = Dialog()
        dialog.show()
        dialog.exec()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    window = MainWindow()    
    window.show()
    sys.exit(app.exec())
