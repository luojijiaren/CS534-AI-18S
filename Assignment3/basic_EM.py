import copy
import numpy as np
from scipy.stats import norm
import pandas as pd
import matplotlib.pyplot as plt
from sys import maxsize as maxint

# Read .csv/.txt both are useful
csv_read = pd.read_csv("/home/jiaming/WPI/CS534/CS534-AI-18S/Assignment3/sample EM data v2.csv")
data = csv_read.values
new_data = np.zeros((len(data),3))


for i in range(len(data)):
    new_data[i][0] = data[i][0]
    new_data[i][1] = data[i][1]

#data = pd.DataFrame({'x':data[0],'y': data[1],'label': np.zeros(len(data[0]))})
#print(data)

x_range = [np.amin(np.transpose(data)[0]), np.amax(np.transpose(data)[0])]
y_range = [np.amin(np.transpose(data)[1]), np.amax(np.transpose(data)[1])]
x_var = np.var(np.transpose(data[0]))
y_var = np.var(np.transpose(data[1]))

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

print("x mean",x_mean)
print("y mean",y_mean)


# initialize the parameter dictionary
for i in range(clsuter_number):
    sub_dict = dict()
    sub_dict['mu'] = [x_mean[i],y_mean[i]];
    sub_dict['sigma'] = [[x_var_array[i],0],[0,y_var_array[i]]]
    para_dict[i+1] = sub_dict

ini_lambda = np.ones(clsuter_number) * (1/clsuter_number)
para_dict['lambda'] = ini_lambda # set the n Gaussian distribution

# Random assign the labels
for i in range(len(new_data)):
    new_data[i][2] = np.random.randint(low=1,high=clsuter_number+1,size=1)

print("new data",new_data)



def probability(value,parameter):

    #important    
    new_para = copy.deepcopy(parameter)
    #log_prob = copy.deepcopy(new_para['lambda'])
    prob = np.ones(len(parameter)-1)
    
    for j in range(len(prob)):
 
        temp_1 = norm.pdf(value[0],new_para[j+1]['mu'][0], new_para[j+1]['sigma'][0][0])
        temp_2 = norm.pdf(value[1],new_para[j+1]['mu'][1], new_para[j+1]['sigma'][1][1])
        
        #print("x prob",temp_1,"y prob",temp_2)
        #print("y prob",temp_2)
        prob[j] = temp_1 * temp_2
        #print("total ",log_prob[j])
            
            #log_prob[j] += value[i]*np.log()
    return prob # 1*3 array

def Expectation(data,parameters_1):
    #prob_list = np.zeros((len(data),3))
    parameters = copy.deepcopy(parameters_1)
    new_data = copy.deepcopy(data)

    for i in range(len(data)):
        x = new_data['x'][i]#data.loc[i,'x']
        y = new_data['y'][i]#data.loc[i,'y']
        prob = probability([x,y],parameters)
        index_ = np.argmax(prob)
        #print("prob list",prob," index:",index_)
        new_data[i][2] = index_
        #prob_list[i] = prob

    return new_data

# def Maximization(data,parameter):
#     # how many labels
#     length = len(parameter)-1

#     new_para = copy.deepcopy(parameter)
#     new_data = copy.deepcopy(data)

#     for i in range(length):
        
#         sub_list 
#         #print("iter,",i+1)
#         #print("sub list",sub_list)
#         #temp_percent = len(sub_dict) / len(data)
#         #new_para['lambda'][i] = temp_percent
#         new_para[i+1]['mu'] = [sub_list['x'].mean(),sub_list['y'].mean()]
#         new_para[i+1]['sigma'] = [[sub_list['x'].std(),0],[0,sub_list['y'].std()]]
    
#     #print(new_para['lambda'])
    
#     return new_para

def distance(past_para_1,new_para_1):
    past_para = copy.deepcopy(past_para_1)
    new_para = copy.deepcopy(new_para_1)
    dist = 0
    length = len(past_para) - 1

    for i in range(length):
        for j in range(0,2):
            dist += (new_para[i+1]['mu'][j] - past_para[i+1]['mu'][j] )**2
    return dist**0.5

# Loop unitil parameters converage
# log-likelihood

def log_likelihood(data,parameter):
    
    sub_length = len(parameter)-1
    length = len(data)

    log_list = np.zeros(3)
    denorm = 0
    expect = np.zeros(3)
    log_likelihood = 0

    for i in range(length):
        
        temp_log_likelihood = 0

        for j in range(sub_length):
            log_list[j] = data['x'][i]*np.log(parameter[j+1]['sigma'][0][0]) + data['y'][i]*np.log(parameter[j+1]['sigma'][1][1])

        for k in range(sub_length):
            denorm += np.exp(log_list[k])*parameter['lambda'][k]
        
        for m in range(sub_length):
            expect[m] = np.exp(log_list[k])*parameter['lambda'][k]/denorm
        
        for k in range(sub_length):
            temp_log_likelihood += expect[k]*log_list[k] 
        
        log_likelihood += temp_log_likelihood

    return log_likelihood

def print_para(para_dict):
    
    for j in range(len(para_dict)-1):
        print (para_dict[j+1]['mu'])
        print (para_dict[j+1]['sigma'])
        print ("------")

shift = 1
epsilon = 0.01
iters = 0
data_copy = copy.deepcopy(data)
paras = copy.deepcopy(para_dict)

""" 
while shift > epsilon:
    iters += 1

    #print("****")
    #print_para(paras)
    #print("****")

    # E-step
    updated_labels = Expectation(data_copy, paras)

    # M-step
    updated_parameters = Maximization(updated_labels, paras)

    
    shift = distance(paras, updated_parameters)
    #print("shift",shift)

    log_value = log_likelihood(updated_labels,updated_parameters)

    #print("log likelihood",log_value)
    #print("shift,",shift)

    # update labels and params for the next iteration
    data_copy = copy.deepcopy(updated_labels)
    paras = copy.deepcopy(updated_parameters)

    #print("****")
    #print_para(paras)
    #print("****")

def make_plot(data,n):
    plt.figure(n)
    plt.scatter(data['x'], data['y'], 24, c=data['label'])
    #plt.show()

data['label'] = 0
make_plot(data,200)

print("Iteration ",iters)

make_plot(data_copy,300)

plt.show()

# # Test Different functions
# prob_list = Expectation(data,para_dict)
# print(prob_list)
# print(para_dict['lambda'])

# BIC equation:
## Equation: BIC_{k}=-2*logL+klogN N is number of observations
# N - number of observations
# k - number of clusters
# logL - log-likelihood

"""