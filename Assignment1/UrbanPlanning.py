#print('Hello')

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
weight_map_1 = []
weight_map_2 = []

for m in range(3,len(iniMap1)):
    for n in range(3,len(iniMap1[m])):
        if iniMap1[m][n] == 'X':
            toxic_1_coord.append([m-2,n+1])

for m in range(3,len(iniMap2)):
    for n in range(3,len(iniMap2[m])):
        if iniMap2[m][n] == 'X':
            toxic_1_coord.append([m-2,n+1])

for m in range(3,len(iniMap1)):
    for n in range(3,len(iniMap1[m])):
        if iniMap1[m][n] == 'S':
            scenic_1_coord.append([m-2,n+1])

for m in range(3,len(iniMap2)):
    for n in range(3,len(iniMap2[m])):
        if iniMap2[m][n] == 'S':
            scenic_2_coord.append([m-2,n+1])

for i in range(3,len(iniMap1)):
    for j in range(3,len(iniMap1[i])):
        weight_map_1.append([i-2,j+1,iniMap1[i][j]])

for i in range(3,len(iniMap2)):
    for j in range(3,len(iniMap2[i])):
        weight_map_2.append([i-2,j+1,iniMap2[i][j]])

class Map:

    def __init__(self,industrial, commerical, residental):
        self.industrial = industrial
        self.commerical = commerical
        self.residental = residental

    def SetToxicSite(self,cooridnates = None):
        if cooridnates is None:
            cooridnates =[]
        self.toxicCoord = cooridnates

    def SetScenicView(self,sceCoord = None):
        if sceCoord is None:
            sceCoord = []
        self.ScenicCoord = sceCoord

    def SetWeightMap(self,weightMap = None):
        if weightMap is None:
            weightMap = []
        self.WeightMap = weightMap

    def SetParentNode(self,ParentNode):
        self.ParentNode = ParentNode

def ManhattanDistance(x1,x2,y1,y2):
    ManDistance = abs(x1-x2) + abs(y1-y2)
    return ManDistance

# Sample 1 Map:
sample_1_Map = Map(iniMap1[0][0],iniMap1[1][0],iniMap1[2][0])
sample_2_Map = Map(iniMap2[0][0],iniMap2[1][0],iniMap2[2][0])
sample_1_Map.SetToxicSite(toxic_1_coord)
sample_1_Map.SetScenicView(scenic_1_coord)
sample_1_Map.SetWeightMap(weight_map_1)
sample_2_Map.SetToxicSite(toxic_2_coord)
sample_2_Map.SetScenicView(scenic_2_coord)
sample_2_Map.SetWeightMap(weight_map_2)

# Hill Climbing
#Take sample 1 as example

# Genetic Algorithm