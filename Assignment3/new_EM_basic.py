import pandas as pd
import numpy as np
import math
import random
import matplotlib.pyplot as plt

file_read = pd.read_csv("sample EM data.csv")
data = file_read.values
data = np.insert(data, 2, 0, axis=1)

#print("data, ",data)

cluster_number = 3 # cluster number

x_range = [np.transpose(data)[0].min(), np.transpose(data)[0].max()]
y_range = [np.transpose(data)[1].min(), np.transpose(data)[1].max()]
x_std = np.std(np.transpose(data)[0])
y_std = np.std(np.transpose(data)[1])

prob_matrix = np.ones((len(data),cluster_number))
prob_matrix = prob_matrix / cluster_number

# Initialize the parameters
para_dict = dict()

point = random.sample(data.tolist(),cluster_number)
point = np.array(point)
print("point",point)
# x_test = np.transpose(point)[0]
# print("x test",x_test)

def generateNumber(low,high,number):

    result = np.zeros(number)
    for i in range(number):
        result[i] = np.random.uniform(low,high,size=1)[0]

    return result

for i in range(len(data)):
    data[i][2] = np.random.randint(0,cluster_number,1)

div_list = []
for j in range(cluster_number):

    sub_list = []
    for i in range(len(data)):
        if data[i][2] == j:
            sub_list.append([data[i][0],data[i][1]])

    div_list.append(sub_list)

print("div list len",len(div_list))

x_std_array = np.zeros(cluster_number)
y_std_array = np.zeros(cluster_number)
x_mean_array = np.zeros(cluster_number)
y_mean_array = np.zeros(cluster_number)

for j in range(cluster_number):
    temp_ = np.array(div_list[j])

    x_std_array[j] = np.std(np.transpose(temp_)[0])
    y_std_array[j] = np.std(np.transpose(temp_)[1])
    idx = np.random.randint(len(div_list[j]), size=1)[0]
    #x_mean_array[j] = div_list[j][idx][0]
    #y_mean_array[j] = div_list[j][idx][1]
    x_mean_array[j] = np.mean(np.transpose(temp_)[0])
    y_mean_array[j] = np.mean(np.transpose(temp_)[1])


# x_mean_array = np.transpose(point)[0]
# y_mean_array = np.transpose(point)[1]
# # x_std_array = np.random.uniform(low = math.pow(x_std,2), high = cluster_number*math.pow(x_std,2)-10, size = (cluster_number,))
# # y_std_array = np.random.uniform(low = math.pow(y_std,2), high = cluster_number*math.pow(y_std,2), size = (cluster_number,))
# x_std_array = generateNumber(5,40,cluster_number)
# y_std_array = generateNumber(30,90,cluster_number)

print("x_mean_array",x_mean_array)
print("y_mean_arry",y_mean_array)
print("x_std",x_std_array)
print("y_std",y_std_array)

## Initialize the parameter dictionary
for i in range(cluster_number):
    sub_dict = dict()
    sub_dict['mu'] = [x_mean_array[i],y_mean_array[i]]
    sub_dict['sigma'] = [[x_std_array[i],0],[0,y_std_array[i]]]
    para_dict[i] = sub_dict
    para_dict['weight'] = np.ones(cluster_number) / cluster_number


def getPDF(value,mu,sigma):

    return (1/(2*math.pi*sigma[0][0]*sigma[1][1]))*np.exp(-math.pow(value[0]-mu[0],2)/(2*math.pow(sigma[0][0],2)))*np.exp(-math.pow(value[1]-mu[1],2)/(2*math.pow(sigma[1][1],2)))

def getCDF(value,mu,sigma):

    return 0.25*(1+math.erf((value[0]-mu[0])/(sigma[0][0]*math.sqrt(2)))) * (1+math.erf((value[1]-mu[1])/(sigma[1][1]*math.sqrt(2))))

def newGetPDF(data,Mu,sigma):

    data = np.array(data)
    Mu = np.array(Mu)
    sigma = np.array(sigma)

    sigma_sqrt = math.sqrt(np.linalg.det(sigma))  # 协方差矩阵绝对值的1/2次
    sigma_inv = np.linalg.inv(sigma)  # 协方差矩阵的逆
    data.shape = (2, 1)
    Mu.shape = (2, 1)
    minus_mu = data - Mu
    minus_mu_trans = np.transpose(minus_mu)
    res = (1.0 / (2.0 * math.pi * sigma_sqrt)) * math.exp(
        (-0.5) * (np.dot(np.dot(minus_mu_trans, sigma_inv), minus_mu)))

    return res

def Expectation(data,para_dict,prob_matrix):

    for i in range(len(data)):
        temp_prob = np.zeros(3)

        # important : multiply the weight
        for j in range(len(para_dict)-1):
            temp_prob[j] = getPDF(data[i][:2],para_dict[j]['mu'],para_dict[j]['sigma']) * para_dict['weight'][j]

        temp_prob = temp_prob/np.sum(temp_prob)
        prob_matrix[i] = temp_prob

    ## Update the probability matrix directly
    #return prob_matrix


def Maximization(data,para_dict,prob_matrix):

    mean_ = np.zeros((len(para_dict)-1,2))
    std_ = np.zeros((len(para_dict)-1,2))
    denom_ = np.zeros(len(para_dict)-1)

    # calculate the denorminator
    for j in range(len(prob_matrix)):
        for i in range(len(para_dict)-1):
            denom_[i] += prob_matrix[j][i]

    ## update mu
    for i in range(len(data)):
        for j in range(len(para_dict)-1):
            mean_[j][0] += data[i][0] * prob_matrix[i][j] / denom_[j]
            mean_[j][1] += data[i][1] * prob_matrix[i][j] / denom_[j]

    ## update sigma
    for i in range(len(data)):
        for j in range(len(para_dict)-1):
            std_[j][0] += math.sqrt(prob_matrix[i][j] * math.pow(data[i][0] - mean_[j][0] ,2) / denom_[j])
            std_[j][1] += math.sqrt(prob_matrix[i][j] * math.pow(data[i][1] - mean_[j][1] ,2) / denom_[j])

    ## Update the weight parameter
    para_dict['weight'] = denom_ / len(data)

    ### Update other parameters
    for i in range(len(para_dict)-1):
        para_dict[i]['mu'] = [mean_[i][0],mean_[i][1]]
        para_dict[i]['sigma'] = [[std_[i][0],0],[0,std_[i][1]]]

    ### Update the parameter dictionary directly
    #return para_dict


'''
for iter in range(100):

    prob_matrix = Expectation(data,para_dict,prob_matrix)

    para_dict = Maximization(data,para_dict,prob_matrix)

print(prob_matrix)

for i in range(len(data)):

    index = np.argmax(prob_matrix[i])
    print(index)
    data[i][2] = index



plt.figure(1)
plt.scatter(np.transpose(data)[0],np.transpose(data)[1],c=np.transpose(data)[2])

plt.figure(2)
plt.scatter(np.transpose(data)[0],np.transpose(data)[1])

plt.show()

'''""

### Test the Expectation function:

## Test the newPDF

test_value = np.array([data[1][0],data[1][1]])
print("shape",test_value.shape)

# sigma_array = np.array(para_dict[1]['sigma'])
# sigma_array = np.power(sigma_array,2)
# print(sigma_array)
# test_new_pdf = newGetPDF([data[1][0],data[1][1]],para_dict[1]['mu'],sigma_array)
# print("result new pdf",test_new_pdf)

test_old_pdf = getPDF([data[1][0],data[1][1]],para_dict[1]['mu'],para_dict[1]['sigma'])
print("result old pdf",test_old_pdf)
# result_pm = Expectation(data,para_dict,prob_matrix)
#
# print(result_pm)
#
#
# ### Test The Maximization function:
#
# result_pd = Maximization(data,para_dict,prob_matrix)
#
# for i in range(cluster_number):
#
#     for subkey in result_pd[i]:
#         print("subkey, ", subkey, '\t', "content", result_pd[i][subkey])
#
# print("Weight vector, ", result_pd['weight'])

# for i in range(100):
#
#     print("Weight vector, ", para_dict['weight'])
#     Expectation(data,para_dict,prob_matrix)
#     Maximization(data,para_dict,prob_matrix)
#     #print("Weight vector, ", para_dict['weight'])


# result_pd = para_dict
#
# for i in range(cluster_number):
#
#     for subkey in result_pd[i]:
#         print("subkey, ", subkey, '\t', "content", result_pd[i][subkey])
#
# print("Weight vector, ", result_pd['weight'])