from particle import Particle
import bif_parser as parser
from sys import maxsize
import math as m
from copy import deepcopy

def ecPSO(numParticles, numNodes, data, completeGraph):
    #import data
    for x in data:
        print(x)
    particles = initParticles(numParticles, numNodes)
    #print(completeGraph)
    numStates = list()
    for node in completeGraph:
        num = completeGraph[node].number
        states = completeGraph[node].getStates()
        numStates.append(deepcopy(states))
    terminate = False
    while not terminate:
        for p in particles:
            p.setVelocity(updateVelocity(p.getVelocity()))
            p = updatePosition(p)
            #if p.getScore() > pbest.getScore():
                #pbest = p.deepcopy()
                #if pbest.getScore() > gbest.getScore():
                    #gbest = pbest.deepcopy()
        terminate = True
    


def insertU(x, y, score, particle, distance, numStates, data):
    #need validity checks
    nx = findNeighbors(x, particle)
    ny = findNeighbors(y, particle)
    nxy = findSharedNeighbors(nx, ny)
    yPi = findParents(y, particle)
    nxy.append(yPi)
    adding = nxy.deepcopy()
    adding.append(x)
    score = score + m.log(calcNodeScore(y,adding, particle, numStates, data)) - m.log(calcNodeScore(y,nxy, particle, numStates, data))
    particle.setScore(score)
    particle.adjMat[x[y]] = 1
    particle.adjMat[y[x]] = 1
    #need to adjust distance
    return particle

def insertD(x, y, score,  particle, distance, numStates, data):
    #need validity checks
    xPi = findParents(x, particle)
    yPi = findParents(y, particle)
    newyPi = yPi.deepcopy()
    newyPi.append(x)
    ny = findNeighbors(y, particle)
    omega = findOmega(xPi, yPi)
    newOmega = omega.deepcopy()
    newOmega.append(newyPi)
    omega.append(yPi)
    score = score + m.log(calcNodeScore(y,newOmega, particle, numStates, data))- m.log(calcNodeScore(y,omega, particle, numStates, data))
    particle.setScore(score)
    particle.adjMat[x[y]] = 1
    particle.adjMat[y[x]] = 0
    #need to adjust distance
    return particle

def deleteD(x, y, score,  particle, distance, numStates, data):
    #need validity checks
    yPi = findParents(y, particle)
    ny = findNeighbors(y, particle)
    newyPi = yPi.deepcopy()
    newyPi.remove(x)
    newNy = ny.deepcopy()
    newNy.append(newyPi)
    ny.append(yPi)
    score = score + m.log(calcNodeScore(y,newNy, particle, numStates, data)) - m.log(calcNodeScore(y,ny, particle, numStates, data))
    particle.setScore(score)
    particle.adjMat[x[y]] = 0
    #need to adjust distance
    return particle

def reverseD(x, y, score,  particle, distance, numStates, data):
    #need validity checks
    yPi = findParents(y, particle)
    newyPi = yPi.deepcopy()
    newyPi.remove(x)

    xPi = findParents(x, particle)
    newxPi = xPi.deepcopy()
    newxPi.append(y)

    nx = findNeighbors(x, particle)
    omega = findOmega(yPi,nx) 
    score = score + m.log((calcNodeScore(y,newyPi, particle, numStates, data) * calcNodeScore(x,newxPi.append(omega), particle, numStates, data))/
                          (calcNodeScore(y,yPi, particle, numStates, data)*calcNodeScore(x,xPi.append(omega), particle, numStates, data)))
    particle.setScore(score)
    particle.adjMat[x[y]] = 0
    particle.adjMat[y[x]] = 0
    #need to adjust distance
    return particle

def deleteU(x, y, score,  particle, distance, numStates, data):
    #need validity checks
    nx = findNeighbors(x, particle)
    ny = findNeighbors(y, particle)
    nxy = findSharedNeighbors(nx, ny)
    yPi = findParents(y, particle)
    nxy.append(yPi)
    removing = nxy.deepcopy()
    removing.append(x)
    score = score + m.log(calcNodeScore(y,nxy, particle, numStates, data)) - m.log(calcNodeScore(y,removing, particle, numStates, data))
    particle.setScore(score)
    particle.adjMat[x[y]] = 0
    particle.adjMat[y[x]] = 0
    #need to adjust distance
    pass

def makeV(x, y, z, score,  particle, distance, numStates, data):
    #need validity checks
    yPi = findParents(y, particle)
    zPi = findParents(x, particle)
    
    nx = findNeighbors(x, particle)
    ny = findNeighbors(y, particle)
    nxy = findSharedNeighbors(nx, ny)

    newzPi = zPi.deepcopy()
    newzPi.append(y)

    newnxy1 = nxy.deepcopy()
    newnxy1.append(x)
    newnxy1.remove(z)
    
    newnxy2 = nxy.deepcopy()
    newnxy2.remove(z)

    last = yPi.deepcopy()
    last.append(nxy)
    score = score + m.log((calcNodeScore(z,newzPi.append(newnxy1), particle, numStates, data) * calcNodeScore(y,yPi.append(newnxy2), particle, numStates, data))/
                          (calcNodeScore(z,zPi.append(newnxy1), particle, numStates, data)*
                           calcNodeScore(y,last, particle, numStates, data)))

    particle.setScore(score)
    particle.adjMat[x[z]] = 1
    particle.adjMat[z[x]] = 0
    particle.adjMat[y[z]] = 1
    particle.adjMat[z[y]] = 0
    #need to adjust distance
    pass

def findParents(x, particle):
    #finds nodes that have directed edges to x
    bigPi = list()
    for n in range(particle.numNodes):
        if n != x:
            if particle.adjMat[n[x]] == 1 and particle.adjMat[x[n]] != 1:
                bigPi.append(n)
    return bigPi

def findNeighbors(x, particle):
    #finds nodes connected to x with undirected edges
    bigN = list()
    for n in range(particle.numNodes):
        if n != x:
            if particle.adjMat[n[x]] == 1 and particle.adjMat[x[n]] == 1:
                bigN.append(n)
    return bigN

def findSharedNeighbors(xNeighborSet, yNeighborSet):
    sharedN = list()
    for i in len(xNeighborSet):
        for j in len(yNeighborSet):
            if xNeighborSet[i] == yNeighborSet[j]:
                sharedN.append(xNeighorSet[i])
    return sharedN

def findOmega(xParentsSet, yNeighborSet):
    bigOmega = list()
    for i in len(xParentsSet):
        for j in len(yNeighborSet):
            if xParentsSet[i] == yNeighborSet[j]:
                bigOmega.append(xNeighorSet[i])
    return bigOmega

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
            topk = m.gamma((10/ri*qi) + Nijk)
            bottomk = m.gamma(10/(ri*qi))
            kscore = kscore * (topk / bottomk)
        jscore = jscore * (topj / bottomj)* kscore
    exp = 0.001 ** ((ri-1)*qi)
    score = exp*jscore
    return score

def calculateScore(particle, numStates, data):
    """returns the BDeu criterion """
    score = 1
    for i in len(particle.adjMat): #i = ith node
        bigPi = findParents(i, particle)
        score = score*calcNodeScore(i, bigPi, particle, numStates, data)
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

def initParticles(numParticles, numNodes):
    particleList = [Particle(numNodes)]*numParticles
    for p in range(numParticles):
        #initialize p with:
            #adjacency matrix
                #generate a random integer randOps
                #for i in randOps:
                    #randomly pick a pair of nodes
                    #if no edge exists between nodes:
                        #randomly select between insertU and insertD
                        #perform selected operators
                    #elif edge is directed:
                        #randomly select between deleteD and reverseD
                        #perform selected operators
                    #elif two undirected edges exist pointing to same node:
                        #randomly select between makeV, deleteU(x,y), and deleteU(y,z)
                        #perform selected operators
                    #else:
                        #randomly select between deleteU and do nothing
                        #perform selected operators
            #chain sub-matrix
                #for n1 in nodes:
                    #for n2 in nodes:
                        #if n1 != n2 AND undirected edge exists between n1 and n2:
                            #add edge to chain sub-matrix
            #initial score
                #calculate score
        #add p to list of particles
        #set pbest of particles to current particle
        pass
    #find best particle  and set to gbest
    for p in range(numParticles):
        #initialize velocity
        pass
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
    ecPSO(5,len(massiveData[0]), massiveData, massiveDictionary)
    #print(massiveData)
    #JANETTE#
    #adjacencyDict is the one you are prolly interested in
    #instead of 50 replace it with how many samples you want
    
if __name__ == "__main__": main()
