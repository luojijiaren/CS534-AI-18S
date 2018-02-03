import random

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
                neighbour[k].append(abs(str[i]-j-1))
                k = k+1
    return neighbour



print('Enter the number of queen:')
N=int(input())
queen=random_list(1,N,N)
neighbour1=find_neighbour(queen,N)

print(queen)
print(neighbour1)


