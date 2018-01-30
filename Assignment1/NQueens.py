import random
import itertools

def iniBoard( length ):
    "This is a initialize function"
    coordinate = []
    x_coordinate = random.sample(range(1,length + 1),length)
    y_coordinate = random.sample(range(1,length + 1),length)

    for i in range(0,length):
        coordinate.append([x_coordinate[i],y_coordinate[i]])
    return coordinate

def heuristicFunction( board ):

    counter = 0
    print("Length : " + str(len(board)))
    length = len(board)
    for i in range(0,len(board)):
        for j in range(i+1,len(board)):
         print("i:" + str(i) + "j:" + str(j))
         print (board[i][0])
         print (board[j][0])
         r1 = board[i][0] - board[j][0]
         r2 = board[i][1] - board[j][1]
         print (abs(r1))
         print (abs(r2))

         if (r1 == r2):
             counter = counter + 1
             print ("counter: xie xian " + str(counter))
             if (counter >= length):
                    counter = length
                    print("counter: exceed 1 " + str(counter))
                    break
         #elif (abs(board[i][0] - board[j][0]) == 0 or abs(board[j][1] - board[j][1] == 0)):
         #    print ("i: " + " " + str(board[i]))
         #    print ("j: " + " " + str(board[j]))
         #    print ("x :" + " " + str(abs(board[i][0] - board[j][0])))
         #    print ("y :" + " " + str(abs(board[i][1] - board[j][1])))
         #    counter = counter + 1
         #    print("counter: zheng huo shu" + str(counter))
         #    if (counter >= length):
         #           counter = length
         #           print("counter: exceeded 2 " + str(counter))
          #          break

    cost_result = 10 + counter;

    return cost_result

result = iniBoard(4)
heuristic_cost = heuristicFunction(result)


print ("Length : " + str(len(result)))
for n in range(0, len(result)):
    print(str(result[n][0]) + " " + str(result[n][1]))

print ("Attack Number :" + str(heuristic_cost - 10))