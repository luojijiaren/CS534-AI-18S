
# define the Bayesian Network
class BayesNet:

    def __init__(self):
        self.nodeDict = dict()

    def addNode(self,node,parentNode,prob,conProb,childNode):
        dictValue = dict()
        dictValue[parentNode] = parentNode
        dictValue[childNode] = childNode
        dictValue[prob] = prob       #list of values, if empty, the conditional node
        dictValue[conProb] = conProb #another dict,
        dictValue[childNode] = childNode #name of the nodes
        self.nodeDict[node] = dictValue



# Initializa the Bayesian Network
bbn = BayesNet()
bbn.addNode("amenities",parentNode=[],prob={"lots":0.3,"little":0.7},conProb={},childNode=["location"])
bbn.addNode("neighborhood",parentNode=[],prob={"bad":0.4,"good":0.6},conProb={},childNode=["location","children"])
bbn.addNode("size",parentNode=[],prob={"small":0.33,"medium":0.34,"large":0.33},conProb={},childNode=["price"])

tempDict = dict()
tempDict[["lots","bad"]] = {"good":0.3,"bad":0.4,"ugly":0.3}
tempDict[["lots","good"]] = {"good":0.8,"bad":0.15,"ugly":0.05}
tempDict[["little","bad"]] = {"good":0.2,"bad":0.4,"ugly":0.4}
tempDict[["little","good"]] = {"good":0.5,"bad":0.35,"ugly":0.15}
bbn.addNode("location",parentNode=["amenities","neighborhood"],prob={},conProb=tempDict,childNode=["age","price"])

tempDict = dict()
tempDict[["bad"]] = {"bad":0.6,"good":0.4}
tempDict[["good"]] = {"bad":0.3,"good":0.7}
bbn.addNode("children",parentNode=["neighborhood"],prob={},conProb=tempDict,childNode=["schools"])

tempDict = dict()
tempDict[["good"]] = {"old":0.3,"new":0.7}
tempDict[["bad"]] = {"old":0.6,"new":0.4}
tempDict[["ugly"]] = {"old":0.9,"new":0.1}
bbn.addNode("age",parentNode=["location"],prob={},conProb=tempDict,childNode=["price"])

tempDict = dict()
tempDict[["bad"]] = {"bad":0.7,"good":0.3}
tempDict[["good"]] = {"bad":0.8,"good":0.2}
bbn.addNode("schools",parentNode=["children"],prob={},conProb=tempDict,childNode=["price"])

tempDict = dict()
tempDict[["good","old","bad","small"]] = {"cheap":0.5,"ok":0.4,"expensive":0.1}
tempDict[["good","old","bad","medium"]] = {"cheap":0.4,"ok":0.45,"expensive":0.15}
tempDict[["good","old","bad","large"]] = {"cheap":0.35,"ok":0.45,"expensive":0.15}

tempDict[["good","old","good","small"]] = {"cheap":0.4,"ok":0.3,"expensive":0.3}
tempDict[["good","old","good","medium"]] = {"cheap":0.35,"ok":0.3,"expensive":0.35}
tempDict[["good","old","good","large"]] = {"cheap":0.3,"ok":0.25,"expensive":0.45}

tempDict[["good","new","bad","small"]] = {"cheap":0.45,"ok":0.4,"expensive":0.15}
tempDict[["good","new","bad","medium"]] = {"cheap":0.4,"ok":0.45,"expensive":0.15}
tempDict[["good","new","bad","large"]] = {"cheap":0.35,"ok":0.45,"expensive":0.2}

tempDict[["good","new","good","small"]] = {"cheap":0.25,"ok":0.3,"expensive":0.45}
tempDict[["good","new","good","medium"]] = {"cheap":0.2,"ok":0.25,"expensive":0.55}
tempDict[["good","new","good","large"]] = {"cheap":0.1,"ok":0.2,"expensive":0.7}

tempDict[["bad","old","bad","small"]] = {"cheap":0.7,"ok":0.299,"expensive":0.001}
tempDict[["bad","old","bad","medium"]] = {"cheap":0.65,"ok":0.33,"expensive":0.02}
tempDict[["bad","old","bad","large"]] = {"cheap":0.65,"ok":0.32,"expensive":0.03}

tempDict[["bad","old","good","small"]] = {"cheap":0.55,"ok":0.35,"expensive":0.1}
tempDict[["bad","old","good","medium"]] = {"cheap":0.5,"ok":0.35,"expensive":0.15}
tempDict[["bad","old","good","large"]] = {"cheap":0.45,"ok":0.4,"expensive":0.15}

tempDict[["bad","new","bad","small"]] = {"cheap":0.6,"ok":0.35,"expensive":0.05}
tempDict[["bad","new","bad","medium"]] = {"cheap":0.55,"ok":0.35,"expensive":0.1}
tempDict[["bad","new","bad","large"]] = {"cheap":0.5,"ok":0.4,"expensive":0.1}

tempDict[["bad","new","good","small"]] = {"cheap":0.4,"ok":0.4,"expensive":0.2}
tempDict[["bad","new","good","medium"]] = {"cheap":0.3,"ok":0.4,"expensive":0.3}
tempDict[["bad","new","good","large"]] = {"cheap":0.3,"ok":0.3,"expensive":0.4}

tempDict[["ugly","old","bad","small"]] = {"cheap":0.8,"ok":0.1999,"expensive":0.0001}
tempDict[["ugly","old","bad","medium"]] = {"cheap":0.75,"ok":0.24,"expensive":0.01}
tempDict[["ugly","old","bad","large"]] = {"cheap":0.75,"ok":0.23,"expensive":0.02}

tempDict[["ugly","old","good","small"]] = {"cheap":0.65,"ok":0.3,"expensive":0.05}
tempDict[["ugly","old","good","medium"]] = {"cheap":0.6,"ok":0.33,"expensive":0.07}
tempDict[["ugly","old","good","large"]] = {"cheap":0.55,"ok":0.37,"expensive":0.08}

tempDict[["ugly","new","bad","small"]] = {"cheap":0.8,"ok":0.1999,"expensive":0.0001}
tempDict[["ugly","new","bad","medium"]] = {"cheap":0.75,"ok":0.24,"expensive":0.01}
tempDict[["ugly","new","bad","large"]] = {"cheap":0.75,"ok":0.23,"expensive":0.02}

tempDict[["ugly","new","good","small"]] = {"cheap":0.8,"ok":0.1999,"expensive":0.0001}
tempDict[["ugly","new","good","medium"]] = {"cheap":0.75,"ok":0.24,"expensive":0.01}
tempDict[["ugly","new","good","large"]] = {"cheap":0.75,"ok":0.23,"expensive":0.02}