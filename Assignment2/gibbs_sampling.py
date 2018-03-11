import numpy as np
import pandas as pd

class BayesNet(object):

    def __init__(self):
        self.NodeDict = dict()

    # One dictionary mapping to another dictionary
    def addNode(self,name,children,parent,cpd,category):
        tempDict = dict()
        tempDict["children"] = children
        tempDict["parent"] = parent
        tempDict["cpd"] = cpd
        tempDict["category"] = category
        self.NodeDict[name] = tempDict




