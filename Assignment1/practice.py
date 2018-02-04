
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


def foo(k,v, fdict={}):
    fdict[k] = v
    print (fdict)

foo(1,2)
foo(3,4)

node_list = []
for i in range(0,5):
    temp_list = []
    for j in range(0,4):
        temp_list.append(i)
    temp_node = Node(temp_list)
    print(temp_node.board)
    node_list.append(temp_node)

for t in range(len(node_list)):
    print(node_list[i].board)