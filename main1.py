import random
import queue
import timeit

# generate a random number*number chessboard with each column has one queen
# input: start and end is the range of the station of each queen
#        number means this chessboard's size is number*number
# output: a 1*N list means the column and row of each queen
def random_list(start, end, number):
    start = int(start)
    end = int(end)
    number = int(abs(number))
    random_list1 = []
    for i in range(number):
        random_list1.append(random.randint(start, end))
    return random_list1

# feature:calculate the attack number of a chessboard
# input: str is a list of the chessboard, number is the th size of chessboard
# output: the number of attack of this board
def attack_number(str, num, attact_num=0):
    for i in range(num):
        for j in range(i+1,num):
            if str[i]==str[j]:
                attact_num=attact_num + 1
            else:
                if abs(i-j)==abs(str[i]-str[j]):
                    attact_num = attact_num + 1
    return attact_num

def a_star_find_neighbour(str,num):
    neighbour=[]
    k = 0
    for i in range(num):
        for j in range(num):
            if (j+1) != str[i]:
                neighbour.append(list(str))
                neighbour[k][i]=j+1
                neighbour[k][-1]=(neighbour[k][-1] + 10 + (str[i]-j-1)*(str[i]-j-1))
                k = k+1
    return neighbour

def hill_climbing(str,num):
    frontier = queue.PriorityQueue()
    frontier.put((0,str))
    frontier_attack = 10000
    current_attack = 0
    while True:
        current1 = frontier.get()
        current = current1[-1]
        frontier.queue.clear()
        current_attack = attack_number(current,num)
        if current_attack == 0:
            result = current #111
            break
        if frontier_attack <= current_attack:
            result=frontier_queen
            break
        frontier_queen=list(current)
        frontier_attack = current_attack
        neighbour = a_star_find_neighbour(current,num)
        for next in neighbour:
            priority = 10*attack_number(next,num)+ 100 + next[num]
            frontier.put((priority,next))
    return result

def restart(str,num):
    i=-1
    result = []
    start = timeit.default_timer()
    while True:
        peak = hill_climbing(str, num)
        result.append(list(peak))
        i=i+1
        end = timeit.default_timer()
        a = attack_number(peak,num)
        if (end-start) > 10 or a == 0:
            break
        str = random_list(1,num,num)
        str.append(0)
    during_time = end-start
    return result,i,during_time

def a_star(str,num,depth):
    sequence = []
    frontier = queue.PriorityQueue()
    frontier.put((0,str))
    cost_so_far = {}
    cost_so_far[tuple(str[0:-1])] = 0
    came_from = {}
    node_deep={}
    node_deep[tuple(str[0:-1])] = 0
    while not frontier.empty():
        current1 = frontier.get()
        current=current1[-1]
        result=list(current)
        if attack_number(current, num) == 0:
            break
        if node_deep[tuple(current[0:-1])]<depth:
            neighbour = a_star_find_neighbour(current,num)
            for next in neighbour:
                new_cost = 10*attack_number(next,num) + 100 + next[num]
                if tuple(next[0:-1]) not in cost_so_far:
                    cost_so_far[tuple(next[0:-1])] = new_cost
                    frontier.put((new_cost,next))
                    came_from[tuple(next[0:-1])] = current[0:-1]
                    node_deep[tuple(next[0:-1])] = node_deep[tuple(current[0:-1])]+1

    sequence.append(result[0:-1])
    k=0
    while True:
        if tuple(sequence[k]) not in came_from:
            break
        back=came_from[tuple(sequence[k])]
        k=k+1
        sequence.append(back)
    node_expanded=len(cost_so_far)
    return result, sequence, node_expanded

def ID_a_star(str,num):
    start = timeit.default_timer()
    node_expanded = 0
    for i in range(num+1):
        result, sequence, node_expanded1 = a_star(str, num, i+1)
        node_expanded = node_expanded+node_expanded1
        if attack_number(result, num)==0:
            break
    end = timeit.default_timer()
    during_time = end - start
    return result, during_time, sequence, node_expanded

print('Enter the number of queen:')
N=int(input())
print('1 for A*, 2 for hill climbing:')
a=int(input())
queen=random_list(1,N,N)
queen.append(0)
print('start sate:',queen[0:-1])
if a==1:
    result,time, sequence, node_expanded = ID_a_star(queen,N)
    print('end state:', result[0:-1])
    print('sequence:',sequence[::-1])
    print('the node expanded vs the length of solution path:%d vs %d'%(node_expanded,len(sequence)))
    print('node expanded:', node_expanded)
elif a==2:
    result,restart_number,time = restart(queen,N)
    print('end state:', result[-1][0:-1])
    print('cost:', result[-1][-1])
    print('number of restart',restart_number)
    print('length:',len(result))
else:
    print('input error')
print("Time used:",time)