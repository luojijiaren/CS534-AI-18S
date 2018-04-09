EMPTY = 0
BLACK = 1
WHITE = 2

from boardUI import Ui_MainWindow
from PyQt5 import QtWidgets, QtGui
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QMainWindow()
    ex = Ui_MainWindow()
    ex.setupUi(w)
    w.show()

    sys.exit(app.exec_())