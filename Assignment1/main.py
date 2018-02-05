import random
import queue
import time

def random_list(start, end, number):
    start = int(start)
    end = int(end)
    number = int(abs(number))
    random_list1 = []
    for i in range(number):
        random_list1.append(random.randint(start, end))
    return random_list1

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
            priority = attack_number(next,num)
            frontier.put((priority,next))

    return result

def a_star(str,num):
    frontier = queue.PriorityQueue()
    frontier.put((0,str))
    cost_so_far = {}
    cost_so_far[tuple(str[0:-1])] = 0
    while not frontier.empty():
        current1 = frontier.get()
        current=current1[-1]
        if attack_number(current, num) == 0:
            result=list(current)
            break
        neighbour = a_star_find_neighbour(current,num)
        for next in neighbour:
            new_cost = attack_number(next,num) + 10 + next[num]
            if tuple(next[0:-1]) not in cost_so_far:
                cost_so_far[tuple(next[0:-1])] = new_cost
                frontier.put((new_cost,next))
    return result


print('Enter the number of queen:')
N=int(input())
print('1 for A*, 2 for hill climbing:')
a=int(input())
queen=random_list(1,N,N)
queen.append(0)
start = time.clock()
if a==1:
    result=a_star(queen,N)
elif a==2:
    result=hill_climbing(queen,N)
    print('attcak:', attack_number(result,N))
else:
    print('input error')
elapsed = (time.clock() - start)
print(queen[0:-1])
print(result[0:-1])
#print('cost=:',result[-1])
print("Time used:",elapsed)