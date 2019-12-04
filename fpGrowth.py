# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 14:27:41 2019
https://blog.csdn.net/Gamer_gyt/article/details/51113753
@author: user
"""

class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}
        
    # increments the count of node appearance   
    def inc(self, numOccur):
        self.count += numOccur
    # display the fp-tree       
    def disp(self, ind = 1):
        print(' ' *ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind + 1)

# main code: create tree

def createTree(dataSet, minSup = 1):
    # first pass : build headerTable
    
    headerTable = {}
    # counts frequency of occurance
    for trans in dataSet:
        for item in trans:
            # dataSet[trans] : times of this trans appear
            # in this case, every trans appears once
            headerTable[item] = headerTable.get(item,0) + dataSet[trans]
    # remove items not meeting minSup
    for k in list(headerTable):
        if headerTable[k] < minSup:
            del(headerTable[k])
    # if headerTable has no key than return none
    freqItemSet = set(headerTable.keys())
    if len(freqItemSet) == 0:
        return None, None
    # add a parameter to store pointers which point to simimar elements
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]
    # create root node
    retTree = treeNode('Null Set', 1, None)
    
    # second pass : create fp-tree
    
    for tranSet,count in dataSet.items():
        # create a dict to record global frequency of every elements
        # and sorting the element by its frequency 
        localD = {}
        for item in tranSet:
            if item in freqItemSet:
                # be careful the [0], because we added the additional parameter before
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            # sorting every element in each list from dataSet
            orderedItems = [v[0] for v in sorted(localD.items(), key = lambda p: p[1], reverse = True )]
            # update the fp-tree
            updateTree(orderedItems, retTree, headerTable, count)
    return retTree, headerTable
    
    
def updateTree(items, inTree, headerTable, count):
    # if items[0] is in the tree , than count+1
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)
    else:
        # items[0] is not in the tree before
        # create a new node
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        # update the headerTable
        
        # if the items[0] pointer in headerTable point to nowhere,
        # then point to the new node
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] == inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
            
    # update the last elements using recursive
    if len(items) > 1 :
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)
        
def updateHeader(nodeToTest, targetNode):
    while(nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode
    

# load data

def loadSimpDat():
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simpDat

def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict

simpDat = loadSimpDat()
initSet = createInitSet(simpDat)

myFPtree, myHeaderTab = createTree(initSet, 3)
myFPtree.disp()        
        
# create prefix path      
def findPrefixPath(basePat, treeNode):
    # create conditional pattern base 
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    
    return condPats

def ascendTree(leafNode, prefixPath):
    if leafNode.parent!= None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)
        print(prefixPath)
        
findPrefixPath('x', myHeaderTab['x'][1])
findPrefixPath('z', myHeaderTab['z'][1])       
findPrefixPath('r', myHeaderTab['r'][1])

        
def ascendTree(leafNode, prefixPath): #ascends from leaf node to root
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)

def findPrefixPath(basePat, treeNode): #treeNode comes from header table
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1: 
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats