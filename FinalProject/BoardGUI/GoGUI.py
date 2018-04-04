
from chess_board import ChessBoard

## Set the length, width, size of the stone
WIDTH = 760
HEIGHT = 760
MARGIN = 20
GRID = (WIDTH - 2 * MARGIN) / (19 - 1)
PIECE = 40 #SIZE OF THE CHESS
EMPTY = 0
BLACK = 1
WHITE = 2

### PyQt Library

import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QPainter
from PyQt5.QtMultimedia import QSound

#----------------------------
# Define Thread for AI
#----------------------------

class AI(QtCore.QThread):
    finishSignal = QtCore.pyqtSignal(int, int)


#----------------------------
# Define Label class
#----------------------------

class Label(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self, e):
        e.ignore()

class Go_(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # The chess board class
        self.chessboard = ChessBoard()

        # Set the background of the chess board
        palette1 = QPalette()
        palette1.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap('./source/board.jpg')))
        self.setPalette(palette1)

        self.setCursor(Qt.OpenHandCursor)

        # Set the size of the GUI

        app = QApplication(sys.argv)

        w = QWidget()
        #w.resize(800, 800)
        w.move(300, 10) # (x,y) The GUI Move to right x, move down y
        w.setWindowTitle('AlamoGo - Group 10')
        w.show()

        sys.exit(app.exec_())

### Start the GUI

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Go_()
    sys.exit(app.exec_())