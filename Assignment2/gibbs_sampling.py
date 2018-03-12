import pandas as pd
from random import randint
import random

class BayesNet(object):

    def __init__(self):
        self.NodeDict = dict()
        self.sampleDict = dict()

    # One dictionary mapping to another dictionary
    def addNode(self,name,children,parents,table,category):
        tempDict = dict()
        tempDict['children'] = children
        tempDict['parent'] = parents
        #tempDict['cpd'] = cpd
        tempDict['category'] = category
        tempDict['categoryNumber'] = len(category)

        index = list()
        items = list()

        for ele in table:
            index.append(ele[0])
            items.append(ele[1])

        if len(parents) > 1:
            index_list = pd.MultiIndex.from_tuples(index, names=parents)
            cpd = pd.DataFrame(data=items, columns=category, index=index_list)

        elif len(parents) == 1 and parents[0] is not None:
            df = pd.DataFrame(data=items, columns=category, index=index)
            df.index.name = parents[0]
            cpd = df

        elif parents[0] is None:
            cpd = pd.DataFrame(data=items, columns=category)

        tempDict['cpd'] = cpd

        self.NodeDict[name] = tempDict

    def get_prob(self,name, evidence=dict(), value=None):
        cpd = self.NodeDict[name]['cpd']

        if len(evidence) != 0:
            levels = list(evidence.keys())
            values = list(evidence.values())

            if value is not None:
                return cpd.xs(values, level=levels)[value]
            else:
                return cpd.xs(values, level=levels)

        # elif len(evidence) == 1:
        #
        #     values = list(evidence.values())
        #     if value is not None:
        #         return cpd.loc[values[0], value]
        #     else:
        #         return cpd.loc[values[0]]

        elif len(evidence) == 0:
            if value is not None:
                return cpd[value]
            else:
                return cpd

    def initialize(self,evidenceDict):

        nodes_all = set(self.NodeDict.keyes())
        evi_node_set = set(evidenceDict.keys())
        other_node_set = nodes_all - evi_node_set

        # set evidence node and their condition
        for key in evidenceDict:
            self.sampleDict[key] = self.NodeDict[key]
            self.sampleDict[key][category] = evidenceDict[key]

        for key in other_node_set:
            temp_cate_list = list(self.NodeDict[key]['category'])
            temp_index = randint(0,len(temp_cate_list)-1)
            self.sampleDict[key] = self.NodeDict[key]
            self.sampleDict[key]['category'] = temp_cate_list[temp_index]

    # random
    def random_pick(self,cate_list, probabilities):
        x = random.uniform(0, 1)
        cumulative_probability = 0.0
        for item, item_probability in zip(cate_list, probabilities):
            cumulative_probability += item_probability
            if x < cumulative_probability:
                break
        return item

    def markov_blanket_cal(self,node):



        return

    def random_sample(self,evidenceDict):

        nodes_all = set(self.NodeDict.keys())
        evi_node_set = set(evidenceDict.keys())
        other_node_set = list(nodes_all - evi_node_set)

        length = len(other_node_set)

        # Sample one node randomly
        index = randint(0,length-1)
        key = other_node_set[index]

        # According the Markov Blanket, calculate the category that it may appear
        prob_list = self.markov_blanket_cal(key)
        category = self.random_pick(list(self.NodeDict[key]['category']),prob_list)
        self.sampleDict[key]['category'] = category



    def gibbs_sampling(self, predictNode, evidenceDict, iteration, discard):

        self.initialize(evidenceDict)
        cat_list = list(self.NodeDict[predictNode]['category'])
        cat_num_list = [0] * len(self.NodeDict[predictNode])

        for i in range(0,iteration):
            self.random_sample(evidenceDict)

            cat_value = self.sampleDict[predictNode]['category']
            temp_position = cat_list.index(cat_value)
            cat_num_list[temp_position] = cat_num_list[temp_position] + 1

        new_cat_num_list = []
        for i in range(0,len(cat_num_list)):
            new_cat_num_list.append(cat_num_list[i]/iteration)

        # output the result values
        return self.NodeDict[predictNode]['category'],new_cat_num_list



network = BayesNet()
network.addNode('amenities',['location'],[None],[((None),(0.3,0.7))],('lots','little'))
network.addNode('neighborhood',['location','children'],[None],[((None),(0.4,0.6))],('bad','good'))
network.addNode('location',['age','price'],['amenities','neighborhood'],[(('lots','bad'),(0.3,0.4,0.3)),(('lots','good'),(0.8,0.15,0.05)),(('little','bad'),(0.2,0.4,0.4)),(('little','good'),(0.5,0.35,0.15))],('good','bad','ugly'))
network.addNode('children',['schools'],['neighborhood'],[(('bad'),(0.6,0.4)),(('good'),(0.3,0.7))],('bad','good'))
network.addNode('size',['price'],[None],[((None,),(0.33,0.34,0.33))],('small','medium','large'))
network.addNode('schools',['price'],['children'],[(('bad'),(0.7,0.3)),(('good'),(0.8,0.2))],('bad','good'))
network.addNode('age',['price'],['location'],[(('good'),(0.3,0.7)),(('bad'),(0.6,0.4)),(('ugly'),(0.9,0.1))],('old','new'))

name = 'price'
children = [None]
parents = ['age','location','schools','size']
cpd = []
cpd.append((('good','old','bad','small'),(0.5,0.4,0.1)))
cpd.append((('good','old','bad','medium'),(0.4,0.45,0.15)))
cpd.append((('good','old','bad','large'),(0.35,0.45,0.2)))

cpd.append((('good','old','good','small'),(0.4,0.3,0.4)))
cpd.append((('good','old','good','medium'),(0.35,0.3,0.35)))
cpd.append((('good','old','good','large'),(0.3,0.25,0.45)))

cpd.append((('good','new','bad','small'),(0.45,0.4,0.15)))
cpd.append((('good','new','bad','medium'),(0.4,0.45,0.15)))
cpd.append((('good','new','bad','large'),(0.35,0.45,0.2)))

cpd.append((('good','new','good','small'),(0.25,0.3,0.45)))
cpd.append((('good','new','good','medium'),(0.2,0.25,0.55)))
cpd.append((('good','new','good','large'),(0.1,0.2,0.7)))

cpd.append((('bad','old','bad','small'),(0.7,0.299,0.001)))
cpd.append((('bad','old','bad','medium'),(0.65,0.33,0.02)))
cpd.append((('bad','old','bad','large'),(0.65,0.32,0.03)))

cpd.append((('bad','old','good','small'),(0.55,0.35,0.1)))
cpd.append((('bad','old','good','medium'),(0.5,0.35,0.15)))
cpd.append((('bad','old','good','large'),(0.45,0.4,0.15)))

cpd.append((('bad','new','bad','small'),(0.6,0.35,0.05)))
cpd.append((('bad','new','bad','medium'),(0.55,0.35,0.1)))
cpd.append((('bad','new','bad','large'),(0.5,0.4,0.1)))

cpd.append((('bad','new','good','small'),(0.4,0.4,0.2)))
cpd.append((('bad','new','good','medium'),(0.3,0.4,0.3)))
cpd.append((('bad','new','good','large'),(0.3,0.3,0.4)))

cpd.append((('ugly','old','bad','small'),(0.8,0.1999,0.0001)))
cpd.append((('ugly','old','bad','medium'),(0.75,0.24,0.01)))
cpd.append((('ugly','old','bad','large'),(0.75,0.23,0.02)))

cpd.append((('ugly','old','good','small'),(0.65,0.3,0.05)))
cpd.append((('ugly','old','good','medium'),(0.6,0.33,0.07)))
cpd.append((('ugly','old','good','large'),(0.55,0.37,0.08)))

cpd.append((('ugly','new','bad','small'),(0.7,0.27,0.03)))
cpd.append((('ugly','new','bad','medium'),(0.64,0.3,0.06)))
cpd.append((('ugly','new','bad','large'),(0.61,0.32,0.07)))

cpd.append((('ugly','new','good','small'),(0.48,0.42,0.1)))
cpd.append((('ugly','new','good','medium'),(0.41,0.39,0.2)))
cpd.append((('ugly','new','good','large'),(0.37,0.33,0.3)))

category = ('cheap','ok','expensive')
network.addNode(name,children,parents,cpd,category)

td = None
# network.get_prob('price',evidence={'size':'small'})
df = network.get_prob('price')
print(df)

