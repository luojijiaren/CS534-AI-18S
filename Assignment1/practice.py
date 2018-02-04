

class Node:
    def __init__(self, board = None):

        self.parent = None
        self.number = 1
        self.G = 0
        self.H = 0

        if board is None:
            board = []
        self.board = board

    def setGH(self,G,H):
        self.G = G
        self.H = H


trial_list = [1,2,3,4]
node_list = []

for i in range(4):
    temp_list = []
    for j in range(4):
        temp_list.clear()
        for m in range(len(trial_list)):
            temp_list.append(trial_list[m])
        temp_list[j] = temp_list[j] + j
    #temp_list[j] = temp_list[j] + 1

    temp_node = Node(temp_list)
    print(temp_node.board)
    node_list.append(temp_node)
    #for m in range(len(node_list)):
    #   print(node_list[m].board)
    #temp_node.board.clear()



for t in range(len(node_list)):
    print(node_list[t].board)

class revs:
    def __init__(self, rev, us, accs=None):
        self.rev = rev
        self.us = us
        if accs is None:
            accs = []
        self.accs = accs

r1 = revs(1, 1)
r2 = revs(2, 2)
r1.accs.append("Hi!")
print(r1.accs) # prints ['Hi!']
print(r2.accs) # prints ['Hi!']

list = [80, 100, 1000,80]
print (min(80,100,1000,80))