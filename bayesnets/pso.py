from particle import Particle
import bif_parser as parser
from sys import maxsize
import math as m
from copy import deepcopy
import random
from decimal import Decimal

def ecPSO(numParticles, numIterations, numNodes, data, completeGraph):
    #import data
    numStates = list()
    for node in completeGraph:
        num = completeGraph[node].number
        states = completeGraph[node].getStates()
        numStates.append(deepcopy(states))
    particles = initParticles(numParticles, numNodes, numStates, data)
    gbest = deepcopy(particles[0])
    pbest = list()
    bestscore = -maxsize
    for pi in particles:
        pbest.append(deepcopy(pi))
        if pi.getScore() > bestscore:
            gbest = deepcopy(pi)
            bestscore = gbest.getScore()
    
    #print(completeGraph)
   
    iteration = 0
    while iteration < numIterations:
        for p in particles:
            pi = particles.index(p)
            p.setVelocity(updateVelocity(p.getVelocity()))
            p = updatePosition(p)
            if p.getScore() > pbest[pi].getScore():
                pbest = deepcopy(p)
                if pbest[pi].getScore() > gbest.getScore():
                    gbest = deepcopy(pbest[pi])
        iteration += 1
    


def insertU(x, y, particle, distance, numStates, data):
    #need validity checks
    nx = findNeighbors(x, particle)
    ny = findNeighbors(y, particle)
    nxy = findSharedNeighbors(nx, ny)
    yPi = findParents(y, particle)
    nxy = appendNoDrama(nxy, yPi)
    adding = deepcopy(nxy)
    adding = appendNoDrama(adding, [x])
    score = particle.getScore()
    score = score + calcNodeScore(y,adding, numStates, data) - calcNodeScore(y,nxy, numStates, data)
    particle.setScore(score)
    particle.adjMat[x][y] = 1
    particle.adjMat[y][x] = 1
    #need to adjust distance
    return particle

def insertD(x, y, particle, distance, numStates, data):
    #need validity checks
    xPi = findParents(x, particle)
    yPi = findParents(y, particle)
    newyPi = deepcopy(yPi)
    newyPi = appendNoDrama(newyPi, [x])
    ny = findNeighbors(y, particle)
    omega = findOmega(xPi, yPi)
    newOmega = deepcopy(omega)
    newOmega = appendNoDrama(newOmega, newyPi)
    omega = appendNoDrama(omega, yPi)
    score = particle.getScore()
    score = score + calcNodeScore(y,newOmega, numStates, data) - calcNodeScore(y,omega, numStates, data)
    particle.setScore(score)
    particle.adjMat[x][y] = 1
    particle.adjMat[y][x] = 0
    #need to adjust distance
    return particle

def deleteD(x, y, particle, distance, numStates, data):
    #need validity checks
    yPi = findParents(y, particle)
    ny = findNeighbors(y, particle)
    newyPi = deepcopy(yPi)
    if x in newyPi:
        newyPi.remove(x)
    newNy = deepcopy(ny)
    newNy = appendNoDrama(newNy, newyPi)
    ny = appendNoDrama(ny, yPi)
    score = particle.getScore()
    score = score + calcNodeScore(y,newNy, numStates, data) - calcNodeScore(y,ny, numStates, data)
    particle.setScore(score)
    particle.adjMat[x][y] = 0
    #need to adjust distance
    return particle

def reverseD(x, y, particle, distance, numStates, data):
    #need validity checks
    yPi = findParents(y, particle)
    newyPi = deepcopy(yPi)
    if x in newyPi:
        newyPi.remove(x)

    xPi = findParents(x, particle)
    newxPi = deepcopy(xPi)
    newxPi = appendNoDrama(newxPi, [y])

    nx = findNeighbors(x, particle)
    omega = findOmega(yPi,nx)
    score = particle.getScore()
    score = score + calcNodeScore(y,newyPi, numStates, data) + calcNodeScore(x,appendNoDrama(newxPi, omega), numStates, data) - calcNodeScore(y,yPi, numStates, data) + calcNodeScore(x,appendNoDrama(xPi, omega), numStates, data)
    particle.setScore(score)
    particle.adjMat[x][y] = 0
    particle.adjMat[y][x] = 0
    #need to adjust distance
    return particle

def deleteU(x, y, particle, distance, numStates, data):
    #need validity checks
    nx = findNeighbors(x, particle)
    ny = findNeighbors(y, particle)
    nxy = findSharedNeighbors(nx, ny)
    yPi = findParents(y, particle)
    nxy = appendNoDrama(nxy, yPi)
    removing = deepcopy(nxy)
    removing = appendNoDrama(removing, [x])
    score = particle.getScore()
    score = score + calcNodeScore(y,nxy, numStates, data) - calcNodeScore(y,removing, numStates, data)
    particle.setScore(score)
    particle.adjMat[x][y] = 0
    particle.adjMat[y][x] = 0
    #need to adjust distance
    pass

def makeV(x, y, z, particle, distance, numStates, data):
    #need validity checks
    yPi = findParents(y, particle)
    zPi = findParents(x, particle)
    
    nx = findNeighbors(x, particle)
    ny = findNeighbors(y, particle)
    nxy = findSharedNeighbors(nx, ny)

    newzPi = deepcopy(zPi)
    newzPi = appendNoDrama(newzPi, [y])

    newnxy1 = deepcopy(nxy)
    newnxy1 = appendNoDrama(newnxy1, [x])
    newnxy1.remove(z)
    
    newnxy2 = deepcopy(nxy)
    newnxy2.remove(z)

    last = deepcopy(yPi)
    last = appendNoDrama(last, nxy)

    score = particle.getScore()
    score=score+calcNodeScore(z,appendNoDrama(newzPi,newnxy1),numStates,data)+calcNodeScore(y,appendNoDrama(yPi,newnxy2),numStates,data)-calcNodeScore(z,appendNoDrama(zPi,newnxy1),numStates,data)+calcNodeScore(y,last,particle,numStates,data)

    particle.setScore(score)
    particle.adjMat[x][z] = 1
    particle.adjMat[z][x] = 0
    particle.adjMat[y][z] = 1
    particle.adjMat[z][y] = 0
    #need to adjust distance
    pass

def findParents(x, particle):
    #finds nodes that have directed edges to x
    bigPi = list()
    for n in range(particle.numNodes):
        if n != x:
            if particle.adjMat[n][x] == 1 and particle.adjMat[x][n] != 1:
                bigPi.append(n)
    return bigPi

def findNeighbors(x, particle):
    #finds nodes connected to x with undirected edges
    bigN = list()
    for n in range(particle.numNodes):
        if n != x:
            if particle.adjMat[n][x] == 1 and particle.adjMat[x][n] == 1:
                bigN.append(n)
    return bigN

def findSharedNeighbors(xNeighborSet, yNeighborSet):
    sharedN = list()
    for i in range(len(xNeighborSet)):
        for j in range(len(yNeighborSet)):
            if xNeighborSet[i] == yNeighborSet[j]:
                sharedN.append(xNeighorSet[i])
    return sharedN

def findOmega(xParentsSet, yNeighborSet):
    bigOmega = list()
    for i in range(len(xParentsSet)):
        for j in range(len(yNeighborSet)):
            if xParentsSet[i] == yNeighborSet[j]:
                bigOmega.append(xNeighorSet[i])
    return bigOmega

def appendNoDrama(set1, set2):
    newset = list()
    for s1 in range(len(set1)):
        if set1[s1] not in newset:
            newset.append(set1[s1])
    for s2 in range(len(set2)):
        if set2[s2] not in newset:
            newset.append(set2[s2])
    return newset

def calculateDistance():
    pass

def updateDistance():
    pass

def updateVelocity(velocity):
    return velocity

def updatePosition(particle):
    #call update score
    return particle

def calcNodeScore(node, parents, numStates, data):
    nt = 1
    #qi = number of configurations of parent set
    qi = 1
    for parent in parents:
        qi = qi*len(numStates[parent])
    #ri = number of states of variable xi
    ri = len(numStates[node])
    #Nijk = number of records in D for which xi = k and bigPi is in the jth configuration
    #Nij = Nijk summed over k
    jscore = 0
    for j in range(qi):
        Nij = findNij(node, j, parents, numStates, data)
        topj = m.lgamma(nt/qi)
        bottomj = m.lgamma((nt/qi)+Nij)
        kscore = 0
        for k in range(ri):
            Nijk = findNijk(node, k, j, parents, numStates, data)
            topk = m.lgamma((nt/ri*qi) + Nijk)
            bottomk = m.lgamma(nt/(ri*qi))
            kscore = kscore + (topk - bottomk)
        jscore = jscore + (topj - bottomj) + kscore
    d = Decimal(0.2 ** ((ri-1)*qi))
    exp = d.ln()
    js = Decimal(jscore)
    score = exp + js
    return score

def calculateScore(particle, numStates, data):
    """returns the BDeu criterion """
    score = 0
    for i in range(len(numStates)): #i = ith node
        bigPi = findParents(i, particle)
        score = score + calcNodeScore(i, bigPi, numStates, data)
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

def initParticles(numParticles, numNodes, numStates, data):
    particleList = [Particle(numNodes)]*numParticles
    for p in particleList:
        r = random.randint(0, 4)
        for it in range(r):
            node1 = random.randint(0, numNodes-1)
            node2 = random.randint(0, numNodes-1)
            while node1 == node2:
                node2 = random.randint(0, numNodes-1)
            print(numNodes, node1, node2, len(p.adjMat), len(p.adjMat[0])) 
            if p.adjMat[node1][node2] == 0 and p.adjMat[node2][node1] == 0:
                r1 = random.random()
                if r1 >= 0.5:
                    insertU(node1, node2, p, [], numStates, data)
                else:
                    insertD(node1, node2, p, [], numStates, data)
            elif p.adjMat[node1][node2] == 1 and p.adjMat[node2][node1] == 0:
                r1 = random.random()
                if r1 >= 0.5:
                    deleteD(node1, node2, p, [], numStates, data)
                else:
                    reverseD(node1, node2, p, [], numStates, data)
            elif p.adjMat[node2][node1] == 1 and p.adjMat[node1][node2] == 0:
                r1 = random.random()
                if r1 >= 0.5:
                    deleteD(node2, node1, p, [], numStates, data)
                else:
                    reverseD(node2, node1, p, [], numStates, data)
            elif p.adjMat[node1][node2] == 1 and p.adjMat[node2][node1] == 1:
                r1 = random.random()
                if r1 >= 0.5:
                    deleteU(node1, node2, p, [], numStates, data)
            #elif two undirected edges exist pointing to same node:
                #randomly select between makeV(x,y,z, p, [], numStates, data), deleteU(x,y, p, [], numStates, data), and deleteU(y,z, p, [], numStates, data)
                #perform selected operators
        for n1 in range(len(p.adjMat)):
            for n2 in range(len(p.adjMat)):
                if n1 != n2:
                    if p.adjMat[n1][n2] == 1 and p.adjMat[n2][n1] == 1:
                        p.chainMat[n1][n2] = 1
                        p.chainMat[n2][n1] = 1
        score = calculateScore(p, numStates, data)
        p.setScore(score)
    return particleList #also how to store pbest and gbest?

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
    
def main():
    p = parser.Parser()
    (massiveDictionary,adjacencyDictionary) = p.fileparser('asia.bif')
    massiveData = p.dataGeneration(massiveDictionary,10) #specify desired number of samples
    ecPSO(5,10, len(massiveData[0]), massiveData, massiveDictionary)
    #print(massiveData)
    #JANETTE#
    #adjacencyDict is the one you are prolly interested in
    #instead of 50 replace it with how many samples you want
    
if __name__ == "__main__": main()
