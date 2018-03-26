import csv
import matplotlib.pyplot as plt
import random
from scipy.stats import multivariate_normal
import numpy as np

def load_data(filename):
    csv_reader = csv.reader(open(filename, encoding='utf-8'))
    raw_data=[]
    for row in csv_reader:
        for i in range(len(row)):
            row[i]=float(row[i])
        raw_data.append(row)
    return raw_data

def set_start(raw_data,k):
    center=[]
    for i in range(k):
        center.append([raw_data[random.randint(0, len(raw_data))], [random.randint(0, 100),random.randint(0, 100)]])
    return center

def phi(Y, mu_k, cov_k):
    norm = multivariate_normal(mean=mu_k, cov=cov_k)
    return norm.pdf(Y)

def expectation(data,center,k):
    cluster=[]
    for j in range(len(data)):
        a=[]
        for i in range(k):
            a.append(phi(data[j], center[i][0], center[i][1]))
        cluster.append(a.index(max(a)))
    return cluster

def maximization(data,cluster,k):
    new_center=[]
    for i in range(k):
        a = []
        for j in range(len(cluster)):
            if cluster[j] == i:
                a.append(data[j])
        mean=np.mean(a, axis=0)
        std=np.std(a, axis=0)
        new_center.append([mean.tolist(),std.tolist()])
    return new_center

def EM(raw_data,center,k):
    for i in range(5):
        cluster = expectation(raw_data, center, k)
        center = maximization(raw_data, cluster, k)
    return center,cluster

k=3
raw_data=load_data('sample EM data v2.csv')
center = set_start(raw_data, k)
center, cluster = EM(raw_data, center, k)

f1 = plt.figure(1)
x = []
y = []
c=['r', 'y', 'g']
color=[]
for i in range(len(raw_data)):
    x.append(raw_data[i][0])
    y.append(raw_data[i][1])
    color.append(c[cluster[i]])
plt.scatter(x, y)

f2 = plt.figure(2)
plt.scatter(x, y, edgecolors=color)
plt.show()