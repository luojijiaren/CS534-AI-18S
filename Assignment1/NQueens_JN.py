import random
import numpy as np
import math
import copy

def iniBoard( length ):
    "This is a initialize function"
    coordinate = []
    # column coordinate, not to be duplicated
    y_coordinate = random.sample(range(1,length + 1),length)
    # row coordinates, duplicate allowed
    x_coordinate = np.random.randint(low = 1, high = length+1, size = length)

    for i in range(0,length):
        coordinate.append([x_coordinate[i],y_coordinate[i]])
    return coordinate

def NumberOfAttackQueens( board ):

    counter = 0
    #print("Length : " + str(len(board)))
    length = len(board)

    for i in range(0,len(board)):
        for j in range(i+1,len(board)):

         r1 = abs(board[i][0] - board[j][0])
         r2 = abs(board[i][1] - board[j][1])
         if r1 == 0 or r2 == 0:
             counter = counter +1
             #print ("Horizontal or Vertical: " + str(counter))
         else:
             if r1 == r2:
                 counter = counter +1
                 #print("Diagonal Line: " + str(counter))

    return counter #return the number of attack queen pairs

# H(n)
def HeuristicFunction ( AttackPairs ):
    return 10 + AttackPairs

class Node:
     board = None
     def __init__(self, board = None):
         self.parent = None
         self.G = 0
         self.H = 0
         if board is None:
             board = []
         self.board = board

     def setParentNode(self,ParentNode):
         self.parent = ParentNode

     def setGH(self,G,H):
         self.G = G
         self.H = H

     def setBoard(self,new_board):
         self.board = new_board

     def newSetBoard(id,ids=None):
         if id:
             ids = list()
             ids.append(id)

         print(ids)

# each node has n*(n-1) successors
def GenerateSuccessor (tNode ):
    successor_set = set()
    length = len(tNode.board)

    for i in range(0,length): #column index
        tempList = []
        temp_x_index = tNode.board[i][0] #row index
        print("temp_x_index:" + str(temp_x_index))
        #tempList.clear()

        for j in range(1,length + 1):
            if j != temp_x_index:
               #deep Copy function...Create a new object here
               tempList = copy.deepcopy(tNode.board)
               tempList[i][0] = j
               G = 10 + math.pow(j-temp_x_index,2)
               H = 10 + NumberOfAttackQueens(tempList)
               tempNode = Node(tempList)
               tempNode.setGH(G,H)
               successor_set.add(tempNode)
    return successor_set

def aStar(InitialNode):

    open_set = []
    current = InitialNode

    open_set.add(current)
    resultNode = Node(InitialNode)

    while open_set:

        current = min(open_set,key=lambda o:o.G + o.H)
        #open_set.remove(current)
        open_set.clear()
        print ("open set size: " + str(len(open_set)))

        if current.H == 10:
            resultNode = current
            break
        else:
            current_successor = GenerateSuccessor(current)
            open_set = open_set | current_successor
            print("Size of Successor set: " + str(len(current_successor)))
            print("Size of open set: " + str(len(open_set)))

    return resultNode

def HillClimbing( InitialNode ):
    open_set = set()
    current = InitialNode

    open_set.add(current)
    resultNode = Node(InitialNode)

    minH = 10
    while open_set:

        current = min(open_set, key=lambda o: o.H)
        # open_set.remove(current)
        open_set.clear()
        print("open set size: " + str(len(open_set)))

        if current.H == 10:
            resultNode = current
            break
        else:
            current_successor = GenerateSuccessor(current)
            open_set = open_set | current_successor
            print("Size of Successor set: " + str(len(current_successor)))
            print("Size of open set: " + str(len(open_set)))

    return resultNode


#result = [[1,1],[2,2],[1,3],[3,5],[4,4]]# iniBoard(5), only for test
result = iniBoard(7)
print ("Initial Board: " + str(result))
node_object = Node()
node_object.setBoard(result)
successor_set = GenerateSuccessor(node_object)

print ("Initial Board: " + str(result))
for n in successor_set:
         print (n.board)
         print (n.H-10)
         #print ("Real H:" + str(NumberOfAttackQueens(n.board)))


current = min(successor_set,key=lambda o:o.H)
print ( "G: " + str(current.G-10) )
#print(len(current))

print (len(successor_set))

result_node = HillClimbing(node_object)
print(result_node.board)
print(NumberOfAttackQueens(result_node.board))