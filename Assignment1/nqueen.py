
from math import *
import sys
import random

x = {}
n = 9
q = {}
for o in range(1, n + 1):
    q[o] = random.randint(0,n);
print(q)

# for i in range(n):
#     min_cost = 2000
#     current_cost = 0
#     for j in range(n):
#         for k in range(i - 1):
#             if  (q[k] == j):
#                 continue
#             elif abs(j - q[k]) == abs(i - k):
#                 continue
#             else: current_cost = 10 + (q[k] - j) ** 2
#         if  current_cost <= min_cost:
#             min_cost = current_cost
#             x[i] = j
# print(x)

def place(k, i):
    if (i in x.values()):
        return False
    j = 1
    while(j < k):
        if abs(x[j]-i) == abs(j-k):
            return False
        j+=1
    # x[k] = i
    # print("ki",k,i)
    return True
def clear_future_blocks(k):
    for i in range(k,n + 1):
       x[i]=None
# def compare_cost(k,i):
#     x[k] = i
#     print(abs(q[k]-x[k]))

def NQueens(k):
    # cc = sys.maxsize
    # print("k =", k)
    for i in range(1, n + 1):
        # print("i =",i)
        clear_future_blocks(k)
        cc = 20000
        if place(k, i):
            # print(10 + (q[k] - i) ** 2)
            # if (abc <= cc):
            #     cc = abc
            x[k] = i
            if (k==n):
                print(x)
                # for j in x:
                #     print (x[j])
                print ('---------')
            else:
                NQueens(k+1)


NQueens(1)
