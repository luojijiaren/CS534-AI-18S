import random
import copy
import queue
from scipy.special import comb
import numpy as np
import timeit
import tkinter as tk
from tkinter import filedialog

class Map:
    def __init__(self,industrial, commercial, residential):
        self.industrial = int(industrial)
        self.commercial = int(commercial)
        self.residential = int(residential)
        self.siteAmount = int(industrial) + int(commercial) + int(residential)

    def setToxicSite(self,cooridnates = None):
        if cooridnates is None:
            cooridnates =[]
        self.toxicCoord = copy.deepcopy(cooridnates)

    def setScenicView(self,sceCoord = None):
        if sceCoord is None:
            sceCoord = []
        self.scenicCoord = copy.deepcopy(sceCoord)

    def setCostMap(self,costMap = None):
        if costMap is None:
            costMap = []
        self.costMap = copy.deepcopy(costMap)

    def setParentNode(self,ParentNode):
        self.ParentNode = ParentNode

    def setScore(self,Score):
        self.score = Score

    def MapSize(self,iniMap):
        self.row = len(iniMap)-3
        self.column = len(iniMap[3])

# Read file through using a dialog

# File Dialog box
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()
fobj = open(file_path)

# x is the total content reading from file
x= []
# the site number, [0] - industrial, [1] - commercial [2] - residential
site_number = []
# scenic view coordinates
scenicPosition = []
# toxic view coordinates
toxicPosition = []

for line in fobj:
    x.append(line.rstrip())

for i in range(0,3):
    temp = int(x[i])
    site_number.append(temp)

cost_map = []
for j in range(3,len(x)):
    line = []
    for m in range(len(x[j])):
        if x[j][m] == 'X':
            cost = 99
            line.append(cost)
            toxicPosition.append([j+1,m+1])
        elif x[j][m] == 'S':
            cost = -1
            line.append(cost)
            scenicPosition.append([j+1,m+1])
        elif x[j][m] != ',':
            cost = int(x[j][m])
            line.append(cost)
    cost_map.append(line)

print("site number :" + str(site_number))
print("cost Map " + str(cost_map))
print("scenic view " + str(scenicPosition))
print("toxic view " + str(toxicPosition))

# Generate the Map 1 (Sample1.txt)
map1 = Map(1,1,1)
map1.setToxicSite([[1,1]])
map1.setScenicView([[2,3]])
map1.setCostMap([[99,1,2,4],[3,4,-1,3],[6,0,2,3]]) #99 means this site is 'X', -1 means this site is 'S'

# map2 = Map(4,2,4)
# map2.setToxicSite([[1,4],[2,2],[3,5]])
# map2.setScenicView([[5,1],[5,3]])
# map2.setCostMap([[2,3,3,99,6],[4,99,3,2,3],[3,0,1,6,99],[7,6,5,8,5],[-1,6,-1,9,1],[4,7,2,6,5]])

map2 = Map(site_number[0],site_number[1],site_number[2])
map2.setToxicSite(toxicPosition)
map2.setScenicView(scenicPosition)
map2.setCostMap(cost_map)

def iniPosition(map):
    position = []
    available_position = []
    num_indus = map.industrial
    num_comme = map.commercial
    num_resid = map.residential

    for i in range(len(map.costMap)):
        for j in range(len(map.costMap[i])):
            if map.costMap[i][j] == -1 or map.costMap[i][j] == 99:
                continue
            else:
                available_position.append((i+1,j+1))

    # choose the positions
    random_position = random.sample(range(0,len(available_position)),map.siteAmount)

    # get the coordinate
    for n in range(len(random_position)):
        position.append([available_position[random_position[n]][0],available_position[random_position[n]][1],0])

    #1 for industrial, 2 for commercial, 3 for residential
    for n in range(num_indus):
        position[n][2] = 1
    for n in range(num_comme):
        position[n+num_indus][2] = 2
    for n in range(num_resid):
        position[n+num_indus+num_comme][2] = 3

    return position

def ManhattanDistance(a,b):
    distance = abs(a[0]-b[0]) + abs(b[1]-a[1])
    return distance

def generateSuccessors (position,ini_avail_position):

    result_position = []
    temp_iap = copy.deepcopy(ini_avail_position)

    for i in range(len(position)):
        for j in range(len(temp_iap)):
            temp_iap = copy.deepcopy(removeSameElement(position[i],temp_iap))

    for n in range(len(position)):
        for m in range(len(temp_iap)):
            temp_position = copy.deepcopy(position)
            temp_position[n][0] = temp_iap[m][0]
            temp_position[n][1] = temp_iap[m][1]
            result_position.append(temp_position)

    return result_position

def removeSameElement(ele,temp):
    result = copy.deepcopy(temp)
    for j in range(len(result)):
        if ele[0] == temp[j][0] and ele[1] == temp[j][1]:
            result.pop(j)
    return result

def getAvailablePosition(map):
    available_position = []
    for i in range(len(map.costMap)):
        for j in range(len(map.costMap[i])):
            if map.costMap[i][j] == -1 or map.costMap[i][j] == 99:
                continue
            else:
                available_position.append([i + 1, j + 1])
    return available_position

# get the system time
def getTime():
    time = timeit.default_timer()
    return time

def calculateScore(map,position):
    score = 0

    #pentaly for within 2 tiles from toxic site
    for i in range(len(position)):
        for j in range(len(map.toxicCoord)):
            if ManhattanDistance(position[i][:-1],map.toxicCoord[j]) <=2 :
                if position[i][2] == 1:
                    score = score - 10
                elif position[i][2] == 2:
                    score = score - 20
                elif position[i][2] == 3:
                    score = score - 20

    #Bonus for near Scenic Site, Residental only
    for m in range(len(position)):
        if position[m][2] == 3:
            for n in range(len(map.scenicCoord)):
                if ManhattanDistance([position[m][0],position[m][1]],map.scenicCoord[n]) <= 2:
                    score = score + 10

    # Construction cost on different sites:
    for nn in range(len(position)):
        cost = map.costMap[position[nn][0] - 1][position[nn][1] - 1]
        score = score - cost

    # I,C,R sites points calculation
    ### First Record the index:
    indus_index = []
    comme_index = []
    resid_index = []

    for l in range(len(position)):
        if position[l][2] == 1:
            indus_index.append(l)
        elif position[l][2] == 2:
            comme_index.append(l)
        elif position[l][2] == 3:
            resid_index.append(l)

    ## industrial site benefit from other industrial sites, 2 tiles 3 points bonus:
    for in_l in range(0,len(indus_index)-1):
        for in_1_2 in range(in_l + 1, len(indus_index)):
            if ManhattanDistance(position[indus_index[in_l]][:-1],position[indus_index[in_1_2]][:-1]) <= 2:
                score = score + 3

    ## Commercial benefit from residential, <= 3, +5:
    for com_l in range(len(comme_index)):
        for res_l in range(len(resid_index)):
            if ManhattanDistance(position[comme_index[com_l]][:-1],position[resid_index[res_l]][:-1]) <= 3:
                score = score + 5

    ## Commercial compete with each other, <=2 , -5
    for com_l_1 in range(0,len(comme_index)-1):
        for com_l_2 in range(com_l_1+1,len(comme_index)):
            if ManhattanDistance(position[comme_index[com_l_1]][:-1],position[comme_index[com_l_2]][:-1]) <=2:
                score = score - 5


    ## Residential near industrial, penalty, <=3, -5
    for res_l_1 in range(len(resid_index)):
        for ind_l_1 in range(len(indus_index)):
            if ManhattanDistance(position[resid_index[res_l_1]][:-1],position[indus_index[ind_l_1]][:-1]) <= 3:
                score = score - 5

    return score

# On the following are functions for Genetic Algorithm
def colonySize(map):

    row = len(map.costMap)
    column = len(map.costMap[0])
    number = row*column
    site_number = map.siteAmount
    colony_size = site_number*(number - site_number)
    return colony_size

def upperBound(map):

    cost_list = []
    for i in range(len(map.costMap)):
        for j in range(len(map.costMap[i])):
            cost_list.append(map.costMap[i][j])

    cost_list.sort()

    while -1 in cost_list:
        cost_list.remove(-1)
    while 99 in cost_list:
        cost_list.remove(99)

    bonus_S = map.residential * len(map.scenicCoord)*10

    bonus_1 = map.residential * map.commercial*5

    if map.industrial >= 2:
        bonus_2 = int(comb(map.industrial,2))*3
    else:
        bonus_2 = 0

    print(bonus_2)

    print(cost_list[:map.siteAmount])
    cost = sum(cost_list[:map.siteAmount])
    print(cost)

    upper_final = bonus_S + bonus_1 + bonus_2 - cost

    return upper_final

def divide(number):
    r1 = 0
    r2 = 0

    if number == 1:
        r1 = 1
        r2 = 1
    elif number % 2 == 0:
        r1 = number / 2
        r2 = number / 2
    elif number % 2 == 1:
        r1 = (number-1)/2
        r2 = (number+1)/2

    r1 = int(r1)
    r2 = int(r2)
    return r1,r2

def getFirstPosition(n,position):
    temp = []
    for i in range(len(position)):
        if position[i][2] == n:
            temp.append(i)

    print("temp :" + str(temp))
    result = temp[0]
    return result

def getPositions(n,position):
    temp = []
    result = []
    for i in range(len(position)):
        if position[i][2] == n:
            temp.append(i)
    result.append(temp[0])
    result.append(temp[-1])
    return result

# Hill Climbing
def hillClimbing (map):

    temp_queue = queue.PriorityQueue()
    ini_position = iniPosition(map)
    available_position = getAvailablePosition(map)
    temp_queue.put((0,ini_position))
    score_list = []
    start = getTime()

    #function upper bound
    upper_bound = upperBound(map)

    #record the value of each restart.
    score_restart = queue.PriorityQueue()

    while True:

        currnt_position = temp_queue.get()[1] #the current position
        previous_score = calculateScore(map,currnt_position)
        temp_queue.queue.clear()

        current_successor = generateSuccessors(currnt_position,available_position)

        del score_list[:]

        for length in range(len(current_successor)):
            temp_score = calculateScore(map,current_successor[length])
            score_list.append(temp_score)
            temp_queue.put((10000-temp_score,current_successor[length]))

        score_list.sort(reverse=True)

        print("Score: " + str(score_list[0]) + " Previous score :" + str(previous_score))


        if score_list[0] <= previous_score:
            time_now = getTime()

            if time_now - start <= 10:
                if score_list[0] < upper_bound:
                    re_ini_pos = iniPosition(map)
                    temp_queue.put((0,re_ini_pos))
                    item = [previous_score,time_now-start]
                    score_restart.put((10000-previous_score,item))
            elif time_now - start > 10:
                result = copy.deepcopy(temp_queue.get()[1])
                item = [previous_score, time_now - start]
                score_restart.put((10000-previous_score,item))
                score = score_restart.get()[1][0]
                time = score_restart.get()[1][1]
                break

    return result,score,time

def selection(scores,population):

    length = len(population)

    for i in range(len(scores)):
        scores[i] = 10000 + scores[i]

    print(scores)

    scores = np.asarray(scores)
    pop_new = np.asarray(population)

    x = np.random.choice(np.arange(length), size=length, replace=True, p = scores/scores.sum())
    pop_new = pop_new[x]
    pop_new = pop_new.tolist()

    return pop_new

def elitism():

    return

def crossOver(parent,n_population,map):

    # get the length
    industrial = map.industrial
    commercial = map.commercial
    residential = map.residential

    # divide the length
    in_1,in_2 = divide(industrial)
    com_1,com_2 = divide(commercial)
    res_1,res_2 = divide(residential)

    inp = 0
    comp = industrial
    resp = industrial + commercial

    #should be the new child

    random_position = random.sample(range(0,len(n_population)),1)
    #print("random position :" + str(random_position))

    pop = copy.deepcopy(n_population[random_position[0]])

    #crossover on Industrial:

    for j in range(inp,inp+in_1):
        #new_parent[inp : inp + in_1-1] = copy.deepcopy(pop[inp + industrial - in_2 : inp + industrial - 1])
        parent[j][0] = copy.deepcopy(pop[inp + industrial - 1 - j][0])
        parent[j][1] = copy.deepcopy(pop[inp + industrial - 1 - j][1])
        parent[j][2] = copy.deepcopy(pop[inp + industrial - 1 - j][2])

    #crossover on commercial:
    for m in range(comp,comp+com_1):
        parent[m][0] = copy.deepcopy(pop[comp + commercial - 1 - m][0])
        parent[m][1] = copy.deepcopy(pop[comp + commercial - 1 - m][1])
        parent[m][2] = copy.deepcopy(pop[comp + commercial - 1 - m][2])

    #new_parent[comp : comp + com_1 - 1] = copy.deepcopy(pop[comp + commercial - com_2 : comp + commercial - 1])

    #crossover on residential:
    for n in range(resp,resp+res_1):
        parent[n][0] = copy.deepcopy(pop[resp + residential - 1 - n][0])
        parent[n][1] = copy.deepcopy(pop[resp + residential - 1 - n][1])
        parent[n][2] = copy.deepcopy(pop[resp + residential - 1 - n][2])

    #new_parent[resp: resp + res_1 - 1] = copy.deepcopy(pop[resp + residential - res_2: resp + residential - 1])

    return parent

def mutation(child, available_position, mutation_rate):

    # between 1 and 3
    #number = random.sample(range(1, 4), 1)

    temp_iap = []
    number = random.sample(range(1, 4), 1)

    if np.random.rand() < mutation_rate:

        for i in range(len(child)):
            for j in range(len(available_position)):
                temp_iap = copy.deepcopy(removeSameElement(child, available_position))

            if number == 1:
                position_range = getPositions(child)
                #position is a list
                position = random.sample(range(position_range[0],position_range[-1]+1),1)

                #random position is also a list
                random_position = random.sample(range(0,len(temp_iap)+1),1)
                child[position[0]][0] = temp_iap[random_position[0]][0]
                child[position[0]][1] = temp_iap[random_position[0]][1]

            elif number == 2:
                position_range = getPositions(child)
                # position is a list
                position = random.sample(range(position_range[0], position_range[-1] + 1), 1)

                # random position is also a list
                random_position = random.sample(range(0, len(temp_iap) + 1), 1)
                child[position[0]][0] = temp_iap[random_position[0]][0]
                child[position[0]][1] = temp_iap[random_position[0]][1]

            elif number == 3:
                position_range = getPositions(child)
                # position is a list
                position = random.sample(range(position_range[0], position_range[-1] + 1), 1)

                # random position is also a list
                random_position = random.sample(range(0, len(temp_iap) + 1), 1)
                child[position[0]][0] = temp_iap[random_position[0]][0]
                child[position[0]][1] = temp_iap[random_position[0]][1]

    return child

def new_mutation(child,map):
    temp_queue = queue.PriorityQueue()
    available_position = getAvailablePosition(map)
    score_list = []

    current_successor = generateSuccessors(child, available_position)

    for length in range(len(current_successor)):
        temp_score = calculateScore(map, current_successor[length])
        score_list.append(temp_score)
        temp_queue.put((10000 - temp_score, current_successor[length]))

    score_list.sort(reverse=True)
    result = copy.deepcopy(temp_queue.get()[1])

    return result


def GeneticAlgorithm(map,generations):

    colony_size = 10#colonySize(map)
    upper = upperBound(map)
    generations = generations
    available_position = getAvailablePosition(map)
    mutation_rate = 1
    score = []
    population = []
    temp_queue = queue.PriorityQueue()

    for _ in range(colony_size):
        population.append(iniPosition(map))

    for __ in range(generations):

        print("-------Loop  -----" + str(__))
        del score[:]
        for index in range(len(population)):
            score.append(calculateScore(map,population[index]))

        #population = selection(score,population)

        # cross over & mutation
        pop_copy = copy.deepcopy(population)
        for l_ in range(len(population)):
            #child = copy.deepcopy(crossOver(population[l_],pop_copy,map))
            child = copy.deepcopy(population[l_])
            #print("child: " + str(child))
            #child = copy.deepcopy(mutation(child,available_position,mutation_rate))

            child = copy.deepcopy(new_mutation(child,map))
            population[l_] = copy.deepcopy(child)

        # mutation

    for j in range(len(population)):
        temp_score = calculateScore(map,population[j])
        temp_queue.put((10000-temp_score,population[j]))

    result = temp_queue.get()

    return result

# Test functions on the following:
#available_position = getAvailablePosition(map2)

# print("")
# print("The Map Idle Positions: ",end="")
# print(available_position)
#
# start = timeit.default_timer()
# result,score = hillClimbing(map2)
# end = timeit.default_timer()
#
# print("The result: ")
# print(result)
# print("The score: "+str(score))
# print("Elpased Time: " + str(end-start))

# print("Colony Size: " + str(colonySize(map2)))
# print("upper bound :" + str(upperBound(map2)))
#

### Genetic Algorithm:

print("Genetic Algorithm: ")
start = timeit.default_timer()
result = GeneticAlgorithm(map2,30)
end = timeit.default_timer()

print("The result: ")
print(result)
print("The score: "+str(10000 - result[0]))
print("Elpased Time: " + str(end-start))

# Hill Climbing:

print("Hill Climbing: ")
start = timeit.default_timer()
result,score,time_1 = hillClimbing(map2)
end = timeit.default_timer()

print("The result: ")
print(result)
print("The score: "+str(score))
print("When achieved: " + str(time_1))
print("Elpased Time: " + str(end-start))

