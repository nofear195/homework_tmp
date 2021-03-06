# -*- coding: utf-8 -*-
"""
reference:
https://blog.csdn.net/Gamer_gyt/article/details/51113753
"""
# construct tree node

class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {} 
    #increments the count variable with a given amount    
    def inc(self, numOccur):
        self.count += numOccur
            
#create FP-tree from dataset
            
def createTree(dataSet, minSup=1):
    headerTable = {}
    
    #first pass counts frequency of occurance
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    for k in list(headerTable):  #remove items not meeting minSup
        if headerTable[k] < minSup: 
            del(headerTable[k])
    freqItemSet = set(headerTable.keys())
    if len(freqItemSet) == 0: return None, None  #if no items meet min support -->get out
    for k in headerTable:
        headerTable[k] = [headerTable[k], None] #reformat headerTable to use Node link 
        
    #create tree    
    retTree = treeNode('Null Set', 1, None) 
    
    # second pass
    for tranSet, count in dataSet.items(): # tranSet = key, count = value
        localD = {}
        for item in tranSet:  #put transaction items in order
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            updateTree(orderedItems, retTree, headerTable, count)#populate tree with ordered freq itemset
    return retTree, headerTable #return tree and header table

def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:#check if orderedItems[0] in retTree.children
        inTree.children[items[0]].inc(count) #incrament count
    else:   #add items[0] to inTree.children
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        if headerTable[items[0]][1] == None: #update header table 
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:#call updateTree() with remaining ordered items
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)
        
def updateHeader(nodeToTest, targetNode):   
    while (nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode
    

# extract conditional pattern base

def findPrefixPath(basePat, treeNode): #treeNode comes from header table
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1: 
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats

def ascendTree(leafNode, prefixPath): #ascends from leaf node to root
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)
        

# mining frequency pattern
        
def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(), key = lambda p: str(p[1]))]
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        myCondTree, myHead = createTree(condPattBases, minSup)
        
        if myHead != None:
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)


# load dataset
            
simpDat = [] 
with open("t2.txt","r") as loadata:
    for line in loadata:
        filtdata = line[5:-1].split(",")
        simpDat += [list(map(str,filtdata))]

def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict

initSet = createInitSet(simpDat)


# run

while True:
    # input minisup
    tmp = input(("input min support or input 'exit' to leave)\n:"))
    if tmp == 'exit':
        break
    else:
        minsup = int(tmp)
        myFPtree, myHeaderTab = createTree(initSet,minsup)
<<<<<<< HEAD:fp_tree_implement.py
        
        # input pattern
        inputset = set(map(str,input("input pattern:").split()))
        # mining frequency pattern
        freqItems = []
        mineTree(myFPtree, myHeaderTab, minsup, set([]), freqItems)
=======
        freqItems = []
        mineTree(myFPtree, myHeaderTab, minsup, set([]), freqItems)
        
        # input pattern
        inputset = set(input("input pattern:").split())
>>>>>>> ee0b0882926a5eae3b94a1bc6dc877bb5920635a:fp_tree_implement.py
        # search if pattern in freqItems and simpDat
        getresult = []
        if inputset in freqItems:
            for line in simpDat:
                for item in line:
                    if item in inputset:
                        getresult.append(simpDat.index(line)+1)
        delduplicates = list(set(getresult))
        finalresult = sorted(delduplicates,key=getresult.index)
        if getresult:
<<<<<<< HEAD:fp_tree_implement.py
            print("index from dataset", finalresult)
=======
            print("index form dataset", finalresult)
>>>>>>> ee0b0882926a5eae3b94a1bc6dc877bb5920635a:fp_tree_implement.py
        else:
            print("None")