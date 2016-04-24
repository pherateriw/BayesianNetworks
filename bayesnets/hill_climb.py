import bif_parser as parser
from sys import maxsize
import math as m
from copy import deepcopy
from collections import OrderedDict
from decimal import Decimal

class HC:
    def __init__(self):
        self.name = 'HC'
    def hillclimb(self, numNodes, data, completeGraph):
        
        edges = list() #create edge list
        edgesprime = list()
        numStates = list()
        for node in completeGraph:
            num = completeGraph[node].number
            states = completeGraph[node].getStates()
            numStates.append(deepcopy(states))
        score = -maxsize #set score to large negative value
        maxscore = score -1
        newscore = maxscore
        while(score > maxscore):
            maxscore = score
            for x in range(len(numStates)):
                #print(x, len(tables[x].getTableGivens()))
                for y in range(len(numStates)):
                    if x != y:
                        if(x,y) in edges and (y,x) not in edges:
                            
                            #print(edges)
                            edgesprime = deepcopy(edges)
                            
                            z = edgesprime.index((x,y))
                            
                            #subtract edge
                            del(edgesprime[z])
                            #recalculate probability tables and score
                            #tablesPrime = recalculateProbTables(edgesprime, tables, tablesprime)
                            newscore = self.calculateScore(edgesprime, numStates, data)
                            if newscore > score:
                                edges = deepcopy(edgesprime)
                                #print(edges)
                                score = newscore
                            #flip edge
                            if not self.detectCycle(x, y, edgesPrime):
                                edgesprime.append((y,x))
                                #recalculate probability tables and score
                                #tablesPrime = recalculateProbTables(edgesprime, tables, tablesprime)
                                newscore = self.calculateScore(edgesprime, numStates, data)
                                if newscore > score:
                                    edges = deepcopy(edgesprime)
                                    score = newscore
                        elif (x,y) not in edges and (y,x) not in edges:
                            edgesPrime = deepcopy(edges)
                            if not self.detectCycle(y, x, edgesPrime):
                                #print(x,y)
                                #add edge
                                edgesprime.append((x,y))
                                #recalculate probability tables and score
                                #tablesPrime = recalculateProbTables(edgesprime, tables, tablesprime)
                                newscore = self.calculateScore(edgesprime, numStates, data)
                                if newscore > score:
                                    edges = deepcopy(edgesprime)
                                    score = newscore
                        elif (x,y) in edges and (y,x) in edges:
                            z = edges.index((x,y))
                            del(edges[z])
                            z2 = edges.index((y,x))
                            del(edges[z2])
            print(score)
        return edges

    def findParents(self, node, edgelist):
        parents = list()
        for pair in edgelist:
            if pair[1] == node:
                if pair[0] not in parents:
                    parents.append(pair[0])
        return parents
                            
    def calcNodeScore(self, node, parents, numStates, data):
        nt = 4
        #qi = number of configurations of parent set
        qi = 1
        for parent in parents:
            #print(parent)
            qi = qi*len(numStates[parent])
        #ri = number of states of variable xi
        ri = len(numStates[node])
        #Nijk = number of records in D for which xi = k and bigPi is in the jth configuration
        #Nij = Nijk summed over k
        jscore = 0
        for j in range(qi):
            Nij = self.findNij(node, j, parents, numStates, data)
            topj = m.lgamma(nt/qi)
            bottomj = m.lgamma((nt/qi)+Nij)
            kscore = 0
            for k in range(ri):
                Nijk = self.findNijk(node, k, j, parents, numStates, data)
                topk = m.lgamma((nt/ri*qi) + Nijk)
                bottomk = m.lgamma(nt/(ri*qi))
                kscore = kscore + (topk - bottomk)
            jscore = jscore + (topj - bottomj) + kscore
        d = Decimal(0.2 ** ((ri-1)*qi))
        exp = d.ln()
        js = Decimal(jscore)
        score = exp + js
        return score

    def calculateScore(self, edgelist, numStates, data):
        """returns the BDeu criterion """
        score = 0
        for i in range(len(numStates)): #i = ith node
            bigPi = self.findParents(i, edgelist)
            score = score + self.calcNodeScore(i, bigPi, numStates, data)
        return score
        
    def findNij(self, i, j, parents, numStates, data):
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
        nij += self.countInstances(data, search, len(data[0]))
        return nij
            
    def findNijk(self, i, k, j, parents, numStates, data):
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
        nijk += self.countInstances(data, search, len(data[0]))
        return nijk

    def detectCycle(self, x, y, edgesList):
        """returns True if there is a directed path from x to y"""
        xtemp = deepcopy(x)
        S = list()
        visited = list()
        S.append(xtemp)
        while len(S) > 0:
            v = S.pop()
            if v == y:
                return True
            if v not in visited:
                visited.append(v)
                for edge in edgesList:
                    if edge[0] == v:
                        S.append(edge[1])
        return False
                  
    def countInstances(self, data, pattern, datalen):
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

