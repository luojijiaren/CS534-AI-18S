import random
import queue

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

def find_neighbour(str,num):
    neighbour = [[] for i in range(num*(num-1))]
    k = 0
    for i in range(num):
        for j in range(num):
            if (j+1) != str[i]:
                neighbour[k] = list(str)
                neighbour[k][i] = j+1
                neighbour[k][num]=neighbour[k][num]+10+(str[i]-j-1)*(str[i]-j-1)
                k = k+1
    return neighbour

def a_star(str,num):
    frontier = queue.PriorityQueue()
    frontier.put(str, 0)
    came_from = {}
    cost_so_far = {}
    came_from[tuple(str[0:-1])] = None
    cost_so_far[tuple(str[0:-1])] = 0

    while not frontier.empty():
        current = frontier.get()
        if attack_number(current, num) == 0:
            result=list(current)
            break
        neighbour = find_neighbour(current,num)
        for next in neighbour:
            new_cost = attack_number(next,num) + 10 + next[num]
            if tuple(next[0:-1]) not in cost_so_far or new_cost < cost_so_far[tuple(next[0:-1])]:
                cost_so_far[tuple(next[0:-1])] = new_cost
                priority = 1000-new_cost
                frontier.put(next, priority)
                came_from[tuple(next[0:-1])] = current
    return result




print('Enter the number of queen:')
N=int(input())
queen=random_list(1,N,N)
queen.append(0)
print(queen[0:-1])
result=a_star(queen,N)
print(result[0:-1])
print('cost=:',result[-1])




