import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# Read .csv/.txt both are useful
csv_read = pd.read_csv("/home/jiaming/WPI/CS534/CS534-AI-18S/Assignment3/sample EM data v2.csv")
data = csv_read.values
data = np.transpose(data)
data = pd.DataFrame({'x':data[0],'y': data[1],'label': np.zeros(len(data[0]))})
#print(data)
x_range = [np.amin(np.array(data['x'])), np.amax(np.array(data['x']))]
y_range = [np.amin(np.array(data['y'])), np.amax(np.array(data['y']))]
x_var = np.var(np.array(data['x']))
y_var = np.var(np.array(data['y']))

# plt.scatter(data['x'],data['y'],7,label=data['label'])#,color='blue')  
# plt.show()

# Now the EM Algorithm
clsuter_number = 3 # ,3 clusters

# Initialize the parameters
para_dict = dict()
x_mean = np.random.uniform(low=x_range[0],high=x_range[1],size=(clsuter_number,))
y_mean = np.random.uniform(low=y_range[0],high=y_range[1],size=(clsuter_number,))
x_var_array = np.random.uniform(low = 0, high = x_var, size = (clsuter_number,))
y_var_array = np.random.uniform(low = 0, high = y_var, size = (clsuter_number,))

print(x_var_array)
print(y_var_array)

# initialize the parameter dictionary
for i in range(clsuter_number):
    sub_dict = dict()
    sub_dict['mu'] = [[x_mean[i],y_mean[i]]];
    sub_dict['sigma'] = [[x_var_array[i],0],[0,y_var_array[i]]]
    para_dict[i+1] = sub_dict

ini_lambda = np.ones(clsuter_number) * (1/clsuter_number)
para_dict['lambda'] = ini_lambda # set the n Gaussian distribution

def probability():
    
    return 
    
def Expectation():

    return 

def Maximization():
    
    return 