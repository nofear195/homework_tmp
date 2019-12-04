# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 15:38:38 2019

@author: user
"""

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
        key = frozenset(trans)
        if retDict.has_key(key):
            retDict[frozenset(trans)] += 1
        else:
            retDict[frozenset(trans)] = 1
    return retDict

simpDat = loadSimpDat()

initSet = createInitSet(simpDat)

class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode      #needs to be updated
        self.children = {} 
#increments the count variable with a given amount    
    def inc(self, numOccur):
        self.count += numOccur
#display tree in text. Useful for debugging        
    def disp(self, ind=1):
        print ('  '*ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind+1)


def createTree(dataSet, minSup=1):
    headerTable = {}
    #go over dataSet twice
    for trans in dataSet:#first pass counts frequency of occurance
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    for k in list(headerTable):  #remove items not meeting minSup
        if headerTable[k] < minSup:
            del(headerTable[k])
    print("headerTable:",headerTable)
    print("headerTable(list)",list(headerTable))
    freqItemSet = set(headerTable.keys())
    print( "freqItemSet :",freqItemSet)
    #print 'freqItemSet: ',freqItemSet
    if len(freqItemSet) == 0: return None, None  #if no items meet min support -->get out
    for k in headerTable:
        headerTable[k] = [headerTable[k], None] #reformat headerTable to use Node link
    print("headerTable",headerTable)
    #print 'headerTable: ',headerTable
    retTree = treeNode('Null Set', 1, None) #create tree
    retTree.disp()
    print("dataSet:",dataSet)
    print("headerTable",headerTable)
    for tranSet, count in dataSet.items():  #go through dataset 2nd time
        # tranSet= key in dict, count = correspond value in dict
        localD = {}
        for item in tranSet:  #put transaction items in order
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        print("localD",localD)
        if len(localD) > 0:
            # reverse order by items count
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            print("orderedItems:",orderedItems)
            updateTree(orderedItems, retTree, headerTable, count)#populate tree with ordered freq itemset
    return retTree, headerTable #return tree and header table

def updateTree(items, inTree, headerTable, count):
    print("items",items)
    print("items[0]",items[0])
    if items[0] in inTree.children:#check if orderedItems[0] in retTree.children
        inTree.children[items[0]].inc(count) #incrament count
        inTree.disp()
    else:   #add items[0] to inTree.children
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        if headerTable[items[0]][1] == None: #update header table 
            headerTable[items[0]][1] = inTree.children[items[0]]
            print("headertableitem",headerTable[items[0]][1])
            print("trr")
            inTree.disp()
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
            print("idtt")
            inTree.disp()
    print("done in tree")
    inTree.disp()
    if len(items) > 1:#call updateTree() with remaining ordered items
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)

def updateHeader(nodeToTest, targetNode):   #this version does not use recursion
    while (nodeToTest.nodeLink != None):    #Do not use recursion to traverse a linked list!
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode



#The FP-tree
myFPtree, myHeaderTab = createTree(initSet, 3)

myFPtree.disp()























