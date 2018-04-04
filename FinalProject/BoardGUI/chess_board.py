
### Define different chess states
EMPTY = 0
BLACK = 1
WHITE = 2

class ChessBoard(object):

    def __init__(self):
        self.board = [[EMPTY for n in range(19)] for m in range(19)]

    def getBoard(self):
        return self.board

    def changeState(self,x,y,state):
        self.board[x][y] = state

    def getState(self,x,y):
        return self.board[x][y]


    def reset(self):
        self.board = [[EMPTY for n in range(19)] for m in range(19)]