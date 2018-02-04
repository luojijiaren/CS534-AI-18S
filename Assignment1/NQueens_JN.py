import random
import numpy as np
import math
import copy
import time

def PrintBoard(coordinate):

    length = len(coordinate)
    pb = [['O'] * length for i in range(length)]

    for m in range(length):
        pb[coordinate[m][0]-1][coordinate[m][1]-1] = 'X'

    for i in range(len(coordinate)):
        if i != 0:
            print("")
        for j in range(len(coordinate)):
            print(str(pb[i][j]), end="")

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
         self.column = 0

     def setParentNode(self,ParentNode):
         self.parent = ParentNode

     def setGH(self,G,H):
         self.G = G
         self.H = H

     def setBoard(self,new_board):
         self.board = new_board

     def setColumn(self,column):
         self.column = column

     def newSetBoard(id,ids=None):
         if id:
             ids = list()
             ids.append(id)

         print(ids)

# each node has n*(n-1) successors
def GenerateSuccessor (tNode ):
    successor_set = set()
    length = len(tNode.board)
    column = tNode.column

    for i in range(0, length):  # column index
        tempList = []
        temp_x_index = tNode.board[i][0]  # row index
        # print("temp_x_index:" + str(temp_x_index))
        # tempList.clear()

        for j in range(1, length + 1):
            if j != temp_x_index:
                # deep Copy function...Create a new object here
                tempList = copy.deepcopy(tNode.board)
                tempList[i][0] = j
                G = 10 + math.pow(j - temp_x_index, 2) + tNode.G
                H = 10 + NumberOfAttackQueens(tempList)
                tempNode = Node(tempList)
                tempNode.setGH(G, H)
                tempNode.setParentNode(tNode)
                successor_set.add(tempNode)
    return successor_set

def GenerateNeighbors_1( tNode ):

    successor_set = set()
    length = len(tNode.board)
    column = tNode.column
    if column == 0:
        for i in range(0, length):  # column index
            tempList = []
            temp_x_index = tNode.board[i][0]  # row index
            # print("temp_x_index:" + str(temp_x_index))
            # tempList.clear()

            for j in range(1, length + 1):
                if j != temp_x_index:
                    # deep Copy function...Create a new object here
                    tempList = copy.deepcopy(tNode.board)
                    tempList[i][0] = j
                    G = 10 + math.pow(j - temp_x_index, 2) + tNode.G
                    H = 10 + NumberOfAttackQueens(tempList)
                    tempNode = Node(tempList)
                    tempNode.setGH(G, H)
                    tempNode.setParentNode(tNode)
                    tempNode.setColumn(i+1)
                    successor_set.add(tempNode)
    else:
        if column == length:
            column == 1
        else:
            column = column + 1

        temp_x_index_2 = tNode.board[column - 1][0]  # row index, next index from Parent Node

        for ln in range(1, length + 1):
            if ln != temp_x_index_2:
                tempList2 = copy.deepcopy(tNode.board)
                tempList2[column - 1][0] = ln
                G = 10 + math.pow(ln - temp_x_index_2, 2) + tNode.G
                H = 10 + NumberOfAttackQueens(tempList2)
                tempNode = Node(tempList2)
                tempNode.setGH(G, H)
                tempNode.setColumn(column)
                tempNode.setParentNode(tNode)
                successor_set.add(tempNode)

    return successor_set



def aStar(InitialNode):

    open_set = set()
    current = InitialNode

    open_set.add(current)
    resultNode = Node(InitialNode)

    while open_set:

        #current = min(open_set,key=lambda o:o.G + o.H)
        current = min(open_set, key=lambda o:o.H)
        open_set.remove(current)
        #open_set.clear()
        print ("open set size: " + str(len(open_set)))

        if current.H == 10:
            resultNode = current
            break
        else:
            current_successor = GenerateSuccessor(current)
            #current_successor = GenerateNeighbors_1(current)
            open_set = open_set | current_successor
            print("Size of Successor set: " + str(len(current_successor)))
            #print("Size of open set: " + str(len(open_set)))

    return resultNode

def HillClimbing( InitialNode ):
    open_set = set()
    current = InitialNode

    open_set.add(current)
    resultNode = Node(InitialNode)

    last_H = 10
    while open_set:

        current = min(open_set, key=lambda o: o.H)
        last_H = 10 + NumberOfAttackQueens(current.board)
        # open_set.remove(current)
        open_set.clear()
        #print("open set size: " + str(len(open_set)))

        if current.H == 10:
            resultNode = current
            break
        else:
            current_successor = GenerateSuccessor(current)
            temp_next_node = min(current_successor, key=lambda o: o.H)
            temp_next_H = 10 + NumberOfAttackQueens(temp_next_node.board)

            if temp_next_H > last_H:
                print("Dead END: Hill Climbing Stuck.")
                break

            open_set = open_set|current_successor
            #print("Size of Successor set: " + str(len(current_successor)))
            #print("Size of open set: " + str(len(open_set)))

    return resultNode


#result = [[1,1],[2,2],[1,3],[3,5],[4,4]]# iniBoard(5), only for test
result = iniBoard(10)
print("Initial Board: " + str(result))
print("Attack Pairs:" + str(NumberOfAttackQueens(result)))
node_object = Node()
node_object.setBoard(result)
PrintBoard(node_object.board)
#successor_set = GenerateSuccessor(node_object)


#Hill climbing
start = time.clock()
result_node = HillClimbing(node_object)
elapsed = (time.clock() - start)
print(result_node.board)
print ("cost :" + str(result_node.G))
print ("Time elapsed: " + str(elapsed))
print("Attack pairs:" + str(NumberOfAttackQueens(result_node.board)))
PrintBoard(result_node.board)
#A-star
# start = time.clock()
# result_node = aStar(node_object)
# elapsed = (time.clock() - start)
# print(result_node.board)
# print ("cost :" + str(result_node.G))
# print ("Time elapsed: " + str(elapsed))
# print("Attack pairs:" + str(NumberOfAttackQueens(result_node.board)))