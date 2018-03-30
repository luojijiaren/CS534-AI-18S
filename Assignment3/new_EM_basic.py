import pandas as pd
import numpy as np
import math
import random
import matplotlib.pyplot as plt
import copy

def getPDF(value,mu,sigma):

    return (1/(2*math.pi*sigma[0][0]*sigma[1][1]))*np.exp(-math.pow(value[0]-mu[0],2)/(2*math.pow(sigma[0][0],2)))*np.exp(-math.pow(value[1]-mu[1],2)/(2*math.pow(sigma[1][1],2)))

def getCDF(value,mu,sigma):

    return 0.25*(1+math.erf((value[0]-mu[0])/(sigma[0][0]*math.sqrt(2)))) * (1+math.erf((value[1]-mu[1])/(sigma[1][1]*math.sqrt(2))))

def newGetPDF(data,Mu,sigma):

    sigma_sqrt = math.sqrt(np.linalg.det(sigma))
    sigma_inv = np.linalg.inv(sigma)
    data.shape = (2, 1)
    Mu.shape = (2, 1)
    minus_mu = data - Mu
    minus_mu_trans = np.transpose(minus_mu)
    res = (1.0 / (2.0 * math.pi * sigma_sqrt)) * math.exp(
        (-0.5) * (np.dot(np.dot(minus_mu_trans, sigma_inv), minus_mu)))

    return res

def Expectation(data,para_dict,prob_matrix):

    for i in range(len(data)):
        temp_prob = np.zeros(len(para_dict)-1)

        # important : multiply the weight
        for j in range(len(para_dict)-1):
            #temp_prob[j] = getPDF(data[i][:2],para_dict[j]['mu'],para_dict[j]['sigma']) * para_dict['weight'][j]
            temp_data = np.array([data[i][0],data[i][1]])
            temp_prob[j] = newGetPDF(temp_data,para_dict[j]['mu'],para_dict[j]['sigma']) * para_dict['weight'][j]
        temp_prob = temp_prob/np.sum(temp_prob)
        prob_matrix[i] = temp_prob

    ## Update the probability matrix directly
    #return prob_matrix

def log_likelihood(prob_matrix):

    log_value = np.zeros(len(prob_matrix[0]))

    for i in range(len(prob_matrix)):
        for j in range(len(prob_matrix[0])):
            log_value[j] += np.log(prob_matrix[i][j])
            #log_value[j] += prob_matrix[i][j]

    sum_log = np.sum(log_value)

    return -sum_log

def Maximization(data,para_dict,prob_matrix):

    mean_ = np.zeros((len(para_dict)-1,2))
    std_ = np.zeros((len(para_dict)-1,2,2))
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
            #std_[j][0] += prob_matrix[i][j] * math.pow(data[i][0] - mean_[j][0] ,2) / denom_[j]
            #std_[j][1] += prob_matrix[i][j] * math.pow(data[i][1] - mean_[j][1] ,2) / denom_[j]
            temp_data = np.array([data[i][0],data[i][1]])
            temp_data.shape = (2,1)
            temp_mean = np.array([para_dict[j]['mu'][0],para_dict[j]['mu'][1]])
            temp_mean.shape = (2,1)
            minus_mu = temp_data - temp_mean
            std_[j] += prob_matrix[i][j] * (minus_mu ) * np.transpose(minus_mu) / denom_[j]
    ## Update the weight parameter
    para_dict['weight'] = denom_ / len(data)

    # for j in range(len(para_dict)-1):
    #     std_[j][0] = math.sqrt(std_[j][0])
    #     std_[j][1] = math.sqrt(std_[j][1])

    ### Update other parameters
    for i in range(len(para_dict)-1):
        para_dict[i]['mu'] = mean_[i]#[mean_[i][0],mean_[i][1]]
        para_dict[i]['sigma'] = std_[i]#[[std_[i][0],0],[0,std_[i][1]]]

    ### Update the parameter dictionary directly
    #return para_dict

def printVariance(para_dict):

    print("-----------------------")
    for j in range(len(para_dict)-1):
        print("*****")
        print("mu, ", para_dict[j]['mu'])
        print("sigma ", para_dict[j]['sigma'])
        print("*****")
    print("-----------------------")

def BICEquation(log_likelihood,K,N):

    return 2*log_likelihood + K*np.log(N)

def EM(data,para_dict,prob_matrix):

    log_value = 0
    log_list = []
    # for i in range(30):
    epsilon = 0.1
    difference = 10
    delta_mu = 3

    while delta_mu > epsilon:
        #print("Weight vector, ", para_dict['weight'])

        delta_mu = 0
        last_para = copy.deepcopy(para_dict)

        Expectation(data,para_dict,prob_matrix)
        Maximization(data,para_dict,prob_matrix)
        log_value = log_likelihood(prob_matrix)
        #printVariance(para_dict)
        #print("log likelihood",log_value)
        log_list.append(log_value)

        now_para = copy.deepcopy(para_dict)

        for i in range(len(para_dict)-1):
            #delta_mu += abs(now_para[i]['mu'][0] - last_para[i]['mu'][0]) + abs(now_para[i]['mu'][1] - last_para[i]['mu'][1])
            delta_mu += math.sqrt(math.pow(now_para[i]['mu'][0] - last_para[i]['mu'][0],2) + math.pow(now_para[i]['mu'][1] - last_para[i]['mu'][1],2))
        #print(delta_mu)


            #if len(log_list) > 2:
            #difference = log_list[len(log_list)-1] - log_list[len(log_list)-2]
    bic = BICEquation(log_list[-1], cluster_number, len(data))

    return log_list[-1],bic

def InitializeParameter(data,cluster_number):

    ### The data
    data = np.insert(data, 2, 0, axis=1)

    for i in range(len(data)):
        data[i][2] = np.random.randint(0, cluster_number, 1)

    prob_matrix = np.ones((len(data),cluster_number))
    prob_matrix = prob_matrix / cluster_number

    # Initialize the parameters
    para_dict = dict()

    point = random.sample(data.tolist(),cluster_number)
    point = np.array(point)
    print("point",point)

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
        x_mean_array[j] = np.mean(np.transpose(temp_)[0])
        y_mean_array[j] = np.mean(np.transpose(temp_)[1])

    ## Initialize the parameter dictionary
    for i in range(cluster_number):
        sub_dict = dict()
        sub_dict['mu'] = np.array([x_mean_array[i],y_mean_array[i]])
        sub_dict['sigma'] = np.array([[math.sqrt(x_std_array[i]),0],[0,math.sqrt(y_std_array[i])]])
        para_dict[i] = sub_dict
        para_dict['weight'] = np.ones(cluster_number) / cluster_number

    return data,para_dict,prob_matrix

def getResult(data,cluster_number):

    data, para_dict, prob_matrix = InitializeParameter(data, cluster_number)
    log_value, bic = EM(data,para_dict,prob_matrix)

    return log_value,bic


def getOptimalNumber(data,X):

    BIC_list = []
    log_value_list = []

    for i in range(2,X+1):
        temp_log_value,temp_bic = getResult(data,i)
        log_value_list.append(temp_log_value)
        BIC_list.append(temp_bic)

    return BIC_list,log_value_list


file_read = pd.read_csv("sample EM data v2.csv")
data = file_read.values

cluster_number = 5

BIC_list,log_list = getOptimalNumber(data,cluster_number)

print("BIC list",BIC_list)
#
# print("BIC ",bic)
# plt.figure()
# plt.plot(log_list)
# plt.show()
#


