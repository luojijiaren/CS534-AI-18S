import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# Read .csv/.txt both are useful
csv_read = pd.read_csv("./sample EM data.csv")
data = csv_read.values
data = np.transpose(data)
data = pd.DataFrame({'x':data[0],'y': data[1],'label': np.zeros(len(data[0]))})
print(data)

plt.scatter(data['x'],data['y'],7,label=data['label'],color='lightblue')  
plt.show()

# Now the EM Algorithm
clsuter_number = 3 # ,3 clusters

# Initialize the parameters
para_dict = dict()