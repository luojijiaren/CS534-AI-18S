import random
import copy
import queue

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

# Generate the Map 1 (Sample1.txt)
map1 = Map(1,1,1)
map1.setToxicSite([[1,1]])
map1.setScenicView([[2,3]])
map1.setCostMap([[99,1,2,4],[3,4,-1,3],[6,0,2,3]]) #99 means this site is 'X', -1 means this site is 'S'

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

# Hill Climbing:
def hillClimbing (map):

    ini_avail_position = []
    for i in range(len(map.costMap)):
        for j in range(len(map.costMap[i])):
            if map.costMap[i][j] == -1 or map.costMap[i][j] == 99:
                continue
            else:
                ini_avail_position.append([i+1,j+1])


    result = []
    return result

def ManhattanDistance(a,b):
    distance = abs(a[0]-b[0]) + abs(b[1]-a[1])
    return distance

def generateSuccessors (position,ini_avail_position):

    result_position = []
    temp_iap = copy.deepcopy(ini_avail_position)

    for i in range(len(position)):
        for j in range(len(temp_iap)):
            temp_iap = copy.deepcopy(removeSameElement(position[i],temp_iap))

    print("Temp_IAP: " + str(temp_iap))

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

# Test functions on the following:
available_position = []
for i in range(len(map1.costMap)):
    for j in range(len(map1.costMap[i])):
        if map1.costMap[i][j] == -1 or map1.costMap[i][j] == 99:
            continue
        else:
            available_position.append([i+1,j+1])

print("Toxic Site:")
print(map1.toxicCoord)
position = iniPosition(map1)
print("The initialized Position: ",end="")
print(position)

print("")
print("The Map Idle Positions: ",end="")
print(available_position)

p2 = generateSuccessors(position,available_position)
print("")
print("The next: available position length: ",end="")
print(len(p2))
print(" The result :",end="")
for i in range(len(p2)):
    print(str(i) + "th Succsessor")
    print(p2[i])
    score = calculateScore(map1,p2[i])
    print("Score: " + str(score))



#  Test Priority Queue

# queue = queue.PriorityQueue()
# l1 = ['X']
# l2 = ['Y']
# l3 = ['Z']
# l4 = ['DD']
# queue.put((1,l1))
# queue.put((2,l2))
# queue.put((5,l3))
# queue.put((3,l4))
#
# while not queue.empty():
#     print(queue.get()[1][0])
#     print()





















