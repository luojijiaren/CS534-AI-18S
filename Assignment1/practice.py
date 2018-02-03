
for i in range(5,5):
    print (i)


class Node:
    def __init__(self, board):
        self.board = board
        self.parent = None
        self.number = 1
        self.G = 0
        self.H = 0

    def setGH(self,G,H):
        self.G = G
        self.H = H

object = Node(2)
object.setGH(10,10)


print(object.G)
print(object.H)


