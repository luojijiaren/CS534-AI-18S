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
map1.setToxicSite([1,1])
map1.setScenicView([2,3])
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

def generateSuccessors (position,ini_avail_position):

    result_position = []
    temp_iap = copy.deepcopy(ini_avail_position)

    for i in range(len(position)):
        for j in range(len(temp_iap)):
            temp_iap = copy.deepcopy(removeSameElement(position[i],temp_iap))


    result_position = copy.deepcopy((temp_iap))

    return result_position

def removeSameElement(ele,temp):
    result = copy.deepcopy(temp)
    for j in range(len(result)):
        if ele[0] == temp[j][0] and ele[1] == temp[j][1]:
            result.pop(j)

    return result

def calculateScore(map,position):
    score = 0

    return score

# Test functions on the following:
available_position = []
for i in range(len(map1.costMap)):
    for j in range(len(map1.costMap[i])):
        if map1.costMap[i][j] == -1 or map1.costMap[i][j] == 99:
            continue
        else:
            available_position.append([i+1,j+1])

position = iniPosition(map1)
print("The initialized Position: ",end="")
print(position)

print("")
print("The Map Idle Positions: ",end="")
print(available_position)

p2 = generateSuccessors(position,available_position)
print("")
print("The next: available position: ",end="")
print(p2)

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





















