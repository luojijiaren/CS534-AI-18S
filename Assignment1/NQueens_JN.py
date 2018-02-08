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
    print("")

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
         self.ParentCost = 0
         self.differenceG = 0
         self.differenceH = 0

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

     def GetParentCost(self, pcost):
         self.ParentCost = pcost

     def setDifferenceGH(self, differH):
         self.differenceH = differH
         #self.differenceH = differH

     def setH(self,H):
         self.H = H

     def setG(self,G):
         self.G = G



# each node has n*(n-1) successors
def GenerateSuccessor ( tNode ):
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
                #G = 10 + math.pow(j - temp_x_index, 2) + tNode.G
                #print("G of parentNode:" + str(tNode.G))
                H = 10 + NumberOfAttackQueens(tempList)

                tempNode = Node(tempList)
                tempNode.setH(H)
                tempNode.setParentNode(tNode)
                tempNode.GetParentCost(tNode.G)

                #difference G and difference H
                #differH = tNode.H - H
                #tempNode.setDifferenceGH(differH)
                successor_set.add(tempNode)

    return successor_set

def CalculateCost(board1,board2):
    cost = 0
    for i in range(len(board1)):
        if(board1[i][0] != board2[i][0]):
            cost = cost + 10 + math.pow(board1[i][0] - board2[i][0],2)

    return cost



def IsBoardSme(board1,board2):

    for i in range(len(board1)):
        if (board1[i][0] == board2[i][0]):
            break
            return False
        else:
            return True


def aStar(InitialNode):

    open_set = set()
    close_set = set()
    close_list = []
    current = InitialNode

    open_set.add(current)
    resultNode = Node(InitialNode)


    while open_set:

        #expected_node = min(open_set,key=lambda o:o.H)
        for key in open_set:
             if key.H == 10:
                print("Find someone suitable in open set. No need to explore")
                resultNode = key
                open_set.clear()
                break
        if (len(open_set) == 0):
             break

        #print ("Need to explore again")
        current = min(open_set, key=lambda o:o.G + o.H)
        open_set.clear()

        #print("Parent Node G:" + str(current.ParentCost))
        #print("G:" + str(current.G) + " H: " + str(current.H))
        #open_set.clear()
        #print ("open set size: " + str(len(open_set)))

        if current.H == 10:
            resultNode = current
            break
        else:
            current_successor = GenerateSuccessor(current)
            #close_set = close_set | current_successor
            print("Length of current successor:" + str(len(current_successor)))

            temp_set = set()
            for node in current_successor:
                for board in close_list:
                    if IsBoardSme(node.board,board) == True:
                        print("Board same")
                        temp_set.add(node)

            print("Temp set size: " + str(len(temp_set)) + "Current Successor set size : " + str(len(current_successor)))
            current_successor = current_successor - temp_set

            print("After removal: Length of current successor:" + str(len(current_successor)))
            close_set.add(current)
            close_list.append(current.board)

            for key in current_successor:
                new_G = CalculateCost(key.board,InitialNode.board)
                key.setG(new_G)

            #current_successor = GenerateNeighbors_1(current)
            open_set = open_set | current_successor
            #print("Size of Successor set: " + str(len(current_successor)))
            #print("Size of open set: " + str(len(open_set)))

    return resultNode

def HillClimbing( InitialNode ):
    open_set = set()
    current = InitialNode

    open_set.add(current)
    resultNode = Node(InitialNode)

    last_H = 10
    while open_set:

        current = min(open_set, key=lambda o:o.H)
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


#result = [[2, 8], [6, 5], [8, 4], [10, 2], [3, 9], [8, 1], [1, 3], [2, 10], [4, 7], [5, 6]]# iniBoard(5), only for test
result = iniBoard(7)
print("Initial Board: " + str(result))
print("Attack Pairs:" + str(NumberOfAttackQueens(result)))
node_object = Node()
node_object.setBoard(result)
PrintBoard(node_object.board)
#successor_set = GenerateSuccessor(node_object)


#Hill climbing
# start = time.clock()
# result_node = HillClimbing(node_object)
# elapsed = (time.clock() - start)
# print(result_node.board)
# print ("cost :" + str(result_node.G))
# print ("Time elapsed: " + str(elapsed))
# print("Attack pairs:" + str(NumberOfAttackQueens(result_node.board)))
# PrintBoard(result_node.board)

#A-star

start = time.clock()
result_node = aStar(node_object)
elapsed = (time.clock() - start)
print(result_node.board)
print ("cost :" + str(result_node.G))
print ("Time elapsed: " + str(elapsed))
print("Attack pairs:" + str(NumberOfAttackQueens(result_node.board)))
PrintBoard(result_node.board)

