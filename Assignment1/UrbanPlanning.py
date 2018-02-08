#print('Hello')
import copy
import queue
import random
#class Map:

file1 = open("sample 1.txt")
file2 = open("sample 2.txt")
list1 = file1.readlines()
list2 = file2.readlines()
iniMap1 = []
iniMap2 = []

for i in range(len(list2)):
    iniMap2.append((list2[i].rstrip('\n').split(',')))

for j in range(len(list1)):
    iniMap1.append(list1[j].rstrip('\n').split(','))

toxic_1_coord = []
toxic_2_coord = []
scenic_1_coord =[]
scenic_2_coord = []
cost_map_1 = []
cost_map_2 = []


for m in range(3,len(iniMap1)):
    for n in range(0,len(iniMap1[m])):
        if iniMap1[m][n] == 'X':
            toxic_1_coord.append([m-2,n+1])
            cost_map_1.append([m-2,n+1,99])
        elif iniMap1[m][n] == 'S':
            scenic_1_coord.append([m-2,n+1])
            cost_map_1.append([m - 2, n + 1, 0])
        else:
            cost_map_1.append([m - 2, n + 1, iniMap1[m][n]])

for m in range(3,len(iniMap2)):
    for n in range(0,len(iniMap2[m])):
        if iniMap2[m][n] == 'X':
            toxic_2_coord.append([m-2,n+1])
            cost_map_2.append([m - 2, n + 1, 99])
        elif iniMap2[m][n] == 'S':
            scenic_2_coord.append([m-2,n+1])
            cost_map_2.append([m - 2, n + 1, 0])
        else:
            cost_map_2.append([m - 2, n + 1, iniMap2[m][n]])

class Map:
    def __init__(self,industrial, commerical, residental):
        self.industrial = int(industrial)
        self.commerical = int(commerical)
        self.residental = int(residental)
        self.siteAmount = int(industrial) + int(commerical) + int(residental)

    def SetToxicSite(self,cooridnates = None):
        if cooridnates is None:
            cooridnates =[]
        self.toxicCoord = copy.deepcopy(cooridnates)

    def SetScenicView(self,sceCoord = None):
        if sceCoord is None:
            sceCoord = []
        self.scenicCoord = copy.deepcopy(sceCoord)

    def SetCostMap(self,costMap = None):
        if costMap is None:
            costMap = []
        self.costMap = copy.deepcopy(costMap)

    def SetParentNode(self,ParentNode):
        self.ParentNode = ParentNode

    def SetScore(self,Score):
        self.score = Score

    def MapSize(self,iniMap):
        self.row = len(iniMap)-3
        self.column = len(iniMap[3])

def ManhattanDistance(x1,x2,y1,y2):
    ManDistance = abs(x1-x2) + abs(y1-y2)
    return ManDistance

def iniPositon(sampleMap):

    position = []
    temp_position = copy.deepcopy(sampleMap.toxicCoord)
    temp_position = temp_position.extend(sampleMap.scenicCoord)

    print("")
    print("Sample Map Toxic Coordinate: ",end="")
    print(sampleMap.toxicCoord)
    print("Sample Map Scenic Coordinate: ",end="")
    print(sampleMap.scenicCoord)
    print("The Union Set:",end="")
    print(temp_position)

    # for i in range(sampleMap.siteAmount):
    #     temp_x = random.sample(range(1,sampleMap.row+1),1)
    #     temp_y = random.sample(range(1,sampleMap.column+1),1)
    #     while True:
    #
    #         print(temp_position)
    #         for i in range(len(temp_position)):
    #             if temp_x == sampleMap.toxicCoord[i][0] and temp_y == sampleMap.toxicCoord[i][1]:
    #                 temp_x = random.sample(range(1, sampleMap.row + 1), 1)
    #                 temp_y = random.sample(range(1, sampleMap.column + 1), 1)
    #             else:
    #                 break
    #
    #     position.append([temp_x,temp_y])

    return position

# Sample 1 Map:
sample_1_Map = Map(iniMap1[0][0],iniMap1[1][0],iniMap1[2][0])
sample_2_Map = Map(iniMap2[0][0],iniMap2[1][0],iniMap2[2][0])
sample_1_Map.SetToxicSite(toxic_1_coord)
sample_1_Map.SetScenicView(scenic_1_coord)
sample_1_Map.SetCostMap(cost_map_1)
sample_1_Map.MapSize(iniMap1)
sample_2_Map.SetToxicSite(toxic_2_coord)
sample_2_Map.SetScenicView(scenic_2_coord)
sample_2_Map.SetCostMap(cost_map_2)
sample_2_Map.MapSize(iniMap2)

print("IniMap1 :",end="")
print(iniMap1)

print("IniMap2 :",end="")
print(iniMap2)

print("Read Map 1:")
print("Map 1 length :" + str(len(sample_1_Map.costMap)))
#def GenerateSuccessors():

for i in range(len(cost_map_1)):
    print("Position: " + str(cost_map_1[i][0]) + " " + str(cost_map_1[i][1]),end=" ")
    print("Weight =" + str(cost_map_1[i][2]),end=" ")

print(" ")
for i in range(len(sample_1_Map.costMap)):
    print("Position: " + str(sample_1_Map.costMap[i][0]) + " " + str(sample_1_Map.costMap[i][1]),end=" ")
    print("Weight =" + str(sample_1_Map.costMap[i][2]),end=" ")
# Hill Climbing
#Take sample 1 as example

def Hill_Climbing (sample_Map):

    #initialize the position






    return



def GenerateSuccessor(position):

    return


def CalculateScore(sample_Map,position):

    return


# Genetic Algorithm


#Test
initialPosition = iniPositon(sample_1_Map)

print(initialPosition)