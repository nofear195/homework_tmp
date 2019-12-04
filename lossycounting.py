# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 17:11:14 2019

@author: user
"""
origindata = open("t2.txt","r").readlines()
simpDat = []
allDat = []
totalnum = 0
for inp in origindata:
    initdata = inp[5:].split(",")
    #tmp = list(map(int,initdata))
    #tmp2 = list(map(str,tmp))
    #simpDat += [tmp2]
    #print(len(initdata))
    totalnum += len(initdata)
    allDat += list(map(int,initdata))
    simpDat += [list(map(int,initdata))]

min_supp = 0.005
min_err = min_supp*0.1
slideWindow = 1/min_err

counter = {}
for tran in simpDat:
    for item in tran:
        if item in counter:
            counter[item] +=1
        else:
            counter[item] = 1
counter
from math import floor, ceil
ceil(totalnum/slideWindow)
for i in range(ceil(totalnum/slideWindow)):
    print(i)
    i +=1
    
for flow in range(0,totalnum,int(slideWindow)):
    splitnum = [0,0]
    for split in range(ceil(totalnum/slideWindow)):
        splitnum[split] = allDat[flow:flow+ int(slideWindow)]














