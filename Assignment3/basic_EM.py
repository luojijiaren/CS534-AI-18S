import copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math


# Read .csv/.txt both are useful
csv_read = pd.read_csv("/home/jiaming/WPI/CS534/CS534-AI-18S/Assignment3/sample EM data v2.csv")
#csv_read = pd.read_csv("sample EM data.csv")
data = csv_read.values

clsuter_number = 3# ,3 clusters

new_data = np.zeros((len(data),clsuter_number))

prob_matrix = np.ones((len(data),clsuter_number))

prob_matrix = prob_matrix * (1/clsuter_number)


print("probability ",prob_matrix)


for i in range(len(data)):
    new_data[i][0] = data[i][0]
    new_data[i][1] = data[i][1]

#data = pd.DataFrame({'x':data[0],'y': data[1],'label': np.zeros(len(data[0]))})
#print(data)

x_range = [np.amin(np.transpose(data)[0]), np.amax(np.transpose(data)[0])]
y_range = [np.amin(np.transpose(data)[1]), np.amax(np.transpose(data)[1])]
x_var = math.sqrt(np.var(np.transpose(data[0])))
y_var = math.sqrt(np.var(np.transpose(data[1])))

# plt.scatter(data['x'],data['y'],7,label=data['label'])#,color='blue')  
# plt.show()

# Now the EM Algorithm
clsuter_number = 3# ,3 clusters

# Initialize the parameters
para_dict = dict()
x_mean = np.random.uniform(low=x_range[0],high=x_range[1],size=(clsuter_number,))
y_mean = np.random.uniform(low=y_range[0],high=y_range[1],size=(clsuter_number,))
x_var_array = np.random.uniform(low = x_var, high = clsuter_number*x_var, size = (clsuter_number,))
y_var_array = np.random.uniform(low = y_var, high = clsuter_number*y_var, size = (clsuter_number,))

print("x mean",x_mean)
print("y mean",y_mean)
print("x_var_array",x_var_array)
print("y_var_array",y_var_array)


# initialize the parameter dictionary
for i in range(clsuter_number):
    sub_dict = dict()
    sub_dict['mu'] = [x_mean[i],y_mean[i]]
    sub_dict['sigma'] = [[x_var_array[i],0],[0,y_var_array[i]]]
    para_dict[i+1] = sub_dict

ini_lambda = np.ones(clsuter_number) * (1/clsuter_number)
para_dict['lambda'] = ini_lambda # set the n Gaussian distribution

# Random assign the labels
for i in range(len(new_data)):
    new_data[i][2] = np.random.randint(low=1,high=clsuter_number+1,size=1)

#print("new data",new_data)

def getPDF(value,mu,sigma):

    return (1/math.sqrt(2*math.pi*math.pow(sigma,2))) * np.exp(-math.pow(value-mu,2)/(2*math.pow(sigma,2)))

def getCDF(value,mu,sigma):

    return 0.5*(1+math.erf((value-mu)/(sigma*math.sqrt(2))))


def probability(value,parameter,prob_matrix,index):

    #important    
    new_para = copy.deepcopy(parameter)
    #log_prob = copy.deepcopy(new_para['lambda'])
    prob = np.ones(len(parameter)-1)
    
    for j in range(len(prob)):
 
        temp_1 = getPDF(value[0],new_para[j+1]['mu'][0],new_para[j+1]['sigma'][0][0])
        temp_2 = getPDF(value[1],new_para[j+1]['mu'][1],new_para[j+1]['sigma'][1][1])

        prob_matrix[index][j] *= temp_1*temp_2
        #print("x prob",temp_1,"y prob",temp_2)
        #print("y prob",temp_2)
        #prob[j] = np.log(temp_1) + np.log(temp_2)
        #prob[j] = temp_1*temp_2#np.log(temp_1) + np.log(temp_2)
        #print("total ",log_prob[j])

    prob = prob_matrix[index]
            #log_prob[j] += value[i]*np.log()
    return prob # 1*3 array

def Expectation(data,parameters_1,prob_matrix):
    #prob_list = np.zeros((len(data),3))
    parameters = copy.deepcopy(parameters_1)
    new_data = copy.deepcopy(data)

    for i in range(len(data)):
        x = new_data[i][0]
        y = new_data[i][1]
        prob = probability([x,y],parameters,prob_matrix,i)
        #print("Probability list ",prob)
        index_ = np.argmax(prob)
        #print("prob list",prob," index:",index_)
        new_data[i][2] = index_ + 1
        #prob_list[i] = prob

    return new_data

def Maximization(data,parameter):
    # how many labels
    length = len(parameter)-1

    new_para = copy.deepcopy(parameter)
    #new_data = copy.deepcopy(data)

    sub_list = []

    for i in range(length):
        temp_list_x = []
        temp_list_y = []

        for j in range(len(data)):
            if data[j][2] == i+1:
                temp_list_x.append(data[j][0])
                temp_list_y.append(data[j][1])
        
        sub_list.append([temp_list_x,temp_list_y])

    #print("length of sublist",len(sub_list))

        
    for j in range(len(sub_list)):
        #print(sub_list[j][0])
        temp_x_mean = np.mean(np.array(sub_list[j][0]))
        temp_y_mean = np.mean(np.array(sub_list[j][1]))
        temp_x_std = math.sqrt(np.var(np.array(sub_list[j][0])))
        temp_y_std = math.sqrt(np.var(np.array(sub_list[j][1])))

        if temp_y_std == 0:
            print("y standard variance is 0")

            temp_y_std = 1

        elif temp_x_std == 0:
            print("x standard variance is 0")
            temp_x_std = 1

        new_para[j+1]['mu'] = [temp_x_mean,temp_y_mean]
        new_para[j+1]['sigma'] = [[temp_x_std,0],[0,temp_y_std]]


    #print(new_para['lambda'])
    
    return new_para

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

    lambda_list = np.zeros(len(parameter)-1)

    for i in range(len(data)):
        for j in range(len(parameter)-1):
            if data[i][2] == j+1:
                lambda_list[j] += 1

    lambda_list = lambda_list/len(data)

    likeli_ = []
    log_value = 0

    for i in range(len(data)):
        temp_log = 0

        for j in range(len(parameter)-1):
            temp_log += lambda_list[j] * ( (data[i][0] - parameter[j+1]['mu'][0])**2 + (data[i][1] - parameter[j+1]['mu'][1])**2 )**0.5

        log_value += temp_log



    log_value = np.log(log_value)


    return log_value

def alter_log_likelihood(data,parameter):

    log_value = 0



    return log_value

def print_para(para_dict):
    
    for j in range(len(para_dict)-1):
        print (para_dict[j+1]['mu'])
        print (para_dict[j+1]['sigma'])
        print ("------")

shift = 1
epsilon = 0.01
iters = 0
data_copy = copy.deepcopy(new_data)
paras = copy.deepcopy(para_dict)

log_value = 0

#print("data:",data_copy)

log_likeli_list = []

while shift > epsilon:
    iters += 1

    #print("****")
    #print_para(paras)
    #print("****")

    # E-step
    updated_labels = Expectation(data_copy, paras,prob_matrix)

    # M-step
    updated_parameters = Maximization(updated_labels, paras)

    
    shift = distance(paras, updated_parameters)
    #print("shift",shift)

    log_value = log_likelihood(updated_labels,updated_parameters)

    #print("log likelihood",log_value)
    print("shift,",shift)
    print("log likelihood",log_value)
    log_likeli_list.append(log_value)

    # update labels and params for the next iteration
    data_copy = copy.deepcopy(updated_labels)
    paras = copy.deepcopy(updated_parameters)

    #print("****")
    #print_para(paras)
    #print("****")

def make_plot(data,n):
    trans_ = np.transpose(data)
    plt.figure(n)
    plt.scatter(trans_[0], trans_[1], 24, c=trans_[2])
    #plt.show()

#data['label'] = 0
original_data = np.zeros((len(new_data),3))

for i in range(len(original_data)):
    original_data[i][0] = data[i][0]
    original_data[i][1] = data[i][1]
    original_data[i][2] = 0

make_plot(original_data,200)

print("Iteration ",iters)

make_plot(data_copy,300)

#plt.show()

plt.figure()
plt.plot(log_likeli_list,color='r')
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
