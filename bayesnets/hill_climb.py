import bif_parser as parser
from sys import maxsize
import math as m
from copy import deepcopy
from collections import OrderedDict

def hillclimb(numNodes, data, completeGraph):
    
    edges = list() #create edge list
    edgesprime = list()
    numStates = list()
    for node in completeGraph:
        num = completeGraph[node].number
        states = completeGraph[node].getStates()
        numStates.append(deepcopy(states))
    score = 0 #set score to large negative value
    maxscore = score -1
    newscore = maxscore
    while(score > maxscore):
        maxscore = score
        for x in range(len(numStates)):
            #print(x, len(tables[x].getTableGivens()))
            for y in range(len(numStates)):
                if x != y:
                    if(x,y) in edges:
                        print((x,y))
                        #subtract edge
                        edgesprime.remove((x,y))
                        #recalculate probability tables and score
                        #tablesPrime = recalculateProbTables(edgesprime, tables, tablesprime)
                        newscore = calculateScore(edgesprime, numStates, data)
                        if newscore > score:
                            edges = edgesprime.deepcopy()
                            score = newscore
                            
                        #flip edge
                        edgesprime.remove((x,y))
                        edgesprime.append((y,x))
                        #recalculate probability tables and score
                        #tablesPrime = recalculateProbTables(edgesprime, tables, tablesprime)
                        newscore = calculateScore(edgesprime, numStates, data)
                        if newscore > score:
                            edges = deepcopy(edgesprime)
                            score = newscore
                    else:
                        print(x,y)
                        #add edge
                        edgesprime.append((x,y))
                        #recalculate probability tables and score
                        #tablesPrime = recalculateProbTables(edgesprime, tables, tablesprime)
                        newscore = calculateScore(edgesprime, numStates, data)
                        if newscore > score:
                            edges = deepcopy(edgesprime)
                            score = newscore

def findParents(node, edgelist):
    parents = list()
    for pair in edgelist:
        if pair[1] == node:
            parents.append(pair[0])
    return parents
                        
def calcNodeScore(node, parents, numStates, data):
    #qi = number of configurations of parent set
    qi = 1
    for parent in parents:
        qi = qi*len(numStates[parent])
    #ri = number of states of variable xi
    ri = len(numStates[node])
    #Nijk = number of records in D for which xi = k and bigPi is in the jth configuration
    #Nij = Nijk summed over k
    jscore = 1
    for j in range(qi):
        Nij = findNij(node, j, parents, numStates, data)
        topj = m.gamma(10/qi)
        bottomj = m.gamma((10/qi)+Nij)
        kscore = 1
        for k in range(ri):
            Nijk = findNijk(node, k, j, parents, numStates, data)
            print(ri, qi, Nijk)
            topk = m.gamma((10/ri*qi) + Nijk)
            bottomk = m.gamma(10/(ri*qi))
            kscore = kscore * (topk / bottomk)
        jscore = jscore * (topj / bottomj)* kscore
    exp = 0.001 ** ((ri-1)*qi)
    score = exp*jscore
    return score

def calculateScore(edgelist, numStates, data):
    """returns the BDeu criterion """
    score = 1
    for i in range(len(numStates)): #i = ith node
        bigPi = findParents(i, edgelist)
        score = score*calcNodeScore(i, bigPi, numStates, data)
    score = m.log(score)
    return score
    
def findNij(i, j, parents, numStates, data):
    #i is a number
    #j corresponds to a state instantiation
    nij = 0
    search = []
    for g in data[0]:
        search.append(None)
    runningj = j
    for p in parents:
        if runningj < len(numStates[p]):
            search[p] = numStates[p][runningj]
        else:
            runningj - len(numStates[p])
            search[p] = numStates[p][-1]
    nij += countInstances(data, search, len(data[0]))
    return nij
        
def findNijk(i, k, j, parents, numStates, data):
    #i is a number
    #j corresponds to a state instantiation
    nijk = 0
    search = []
    for g in data[0]:
        search.append(None)
    search[i] = numStates[i][k]
    runningj = j
    for p in parents:
        if runningj < len(numStates[p]):
            search[p] = numStates[p][runningj]
        else:
            runningj - len(numStates[p])
            search[p] = numStates[p][-1]
    nijk += countInstances(data, search, len(data[0]))
    return nijk

def recalculateProbTables(edgesList, probTables, tablesPrime):
   
    return probTables
                        
def countInstances(data, pattern, datalen):
    count = 0
    for k in data:
        match = True
        for i in range(datalen):
            if pattern[i] is not None and pattern[i] != k[i]:
                match = False
                break
        if match is True:
            count += 1
    return count    

if __name__ == '__main__':
    p = parser.Parser()
    (massiveDictionary,adjacencyDictionary) = p.fileparser('asia.bif')
    #specify desired number of samples
    massiveData = p.dataGeneration(massiveDictionary,10)
    hillclimb(len(massiveData[0]), massiveData, massiveDictionary)
