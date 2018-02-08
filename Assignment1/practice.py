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

    coordinate.append([0,0]) # G and H
    return coordinate

def NumberOfAttackQueens( tboard ):

    board = tboard[:-1]
    counter = 0
    #print("Length : " + str(len(board)))
    length = len(board)

    for i in range(0,len(board)-1):
        for j in range(i+1,len(board)-2):

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


def ReturnList( open_list ):

    min_list = []

    for i in range(0, len(open_list)):
        min_value = open_list[i][-1][0] + open_list[i][-1][1]
        min_list.append(min_value)

    #print(min_list)
    #print("length " + str(len(min_list)))
    position = min_list.index(min(min_list))
    result_list = copy.deepcopy(open_list[position])
    return result_list

def GenerateSuccessor (curren_list):
    successor_list = []

    for i in range(0, len(curren_list)-1):  # column index
        tempList = []
        temp_x_index = curren_list[i][0]  # row index

        for j in range(1, len(curren_list)-1):
            if j != temp_x_index:
                # deep Copy function...Create a new object here
                tempList = copy.deepcopy(curren_list)
                tempList[i][0] = j
                #G = 10 + math.pow(j - temp_x_index, 2) + tNode.G
                #print("G of parentNode:" + str(tNode.G))
                H = 10 + NumberOfAttackQueens(tempList)
                tempList[-1][1] = H
                successor_list.append(tempList)

    return successor_list

def IsBoardSme(board1,board2):

    for i in range(len(board1)):
        if (board1[i][0] == board2[i][0]):
            break
            return False
        else:
            return True


def CalculateCost(board1,board2):
    cost = 0
    for i in range(len(board1)):
        if(board1[i][0] != board2[i][0]):
            cost = cost + 10 + math.pow(board1[i][0] - board2[i][0],2)

    return cost


def A_star( IniBoard ):

    open_list = []
    close_list = []
    result_list = []

    open_list.append(IniBoard)

    while True:

        current_list = ReturnList(open_list)
        accuCost = current_list[-1][0]
        del open_list[:]

        if current_list[-1][1] == 10:
            result_list = current_list
            break
        else:
            successorList = GenerateSuccessor(current_list)

            index_list = []

            for i in range(len(successorList)):
                for j in range(len(close_list)):
                    if IsBoardSme(successorList[i][:-1],close_list[j][:-1]) == True:
                        index_list.append(i)

            index_list = list(set(index_list))
            print("Index List: ")
            print(index_list)

            print("Successor List length:" + str(len(successorList)))

            if len(index_list) != 0:
                print(index_list)
                print("Successor List length:" + str(len(successorList)))
                for index in range(len(index_list)):
                    successorList.pop(index_list[index])


            close_list.append(current_list)

            for i in range(len(successorList)):
                new_G = accuCost + CalculateCost(successorList[i][:-1],current_list[:-1])
                successorList[i][-1][0] = new_G

            open_list = copy.deepcopy(successorList)


    return result_list



initial_board = iniBoard(7)
print(initial_board)
PrintBoard(initial_board[:-1])

result_board = A_star(initial_board)
print(result_board)
PrintBoard(result_board[:-1])