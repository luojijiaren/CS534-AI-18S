import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()
fobj = open(file_path)

x= []
site_number = []


for line in fobj:
    x.append(line.rstrip())
    #print(line.rstrip())

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
        elif x[j][m] == 'S':
            cost = -1
            line.append(cost)
        elif x[j][m] != ',':
            cost = int(x[j][m])
            line.append(cost)
    cost_map.append(line)


print("site number :" + str(site_number))
print("cost Map " + str(cost_map))


# fobj.close()
