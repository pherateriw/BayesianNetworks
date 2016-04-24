from particle import Particle
import bif_parser as parser
from sys import maxsize
import math as m
from copy import deepcopy
import random
from decimal import Decimal
import hill_climb

def ecPSO(phi1, phi2, expl, numParticles, numIterations, numNodes, data, completeGraph):
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
    for pm in particles:
        pbest.append(deepcopy(pm))
        if pm.getScore() > bestscore:
            gbest = deepcopy(pm)
            bestscore = gbest.getScore()
    for pj in range(len(particles)):
        dp = calculateDistance(pbest[pj], particles[pj])
        dg = calculateDistance(gbest, particles[pj])
        particles[pj].setPBestDist(dp)
        particles[pj].setGBestDist(dg)
    #print(completeGraph)
   
    iteration = 0
    while iteration < numIterations:
        print(gbest.getScore())
        for p in particles:
            pi = particles.index(p)
            p = updatePosition(phi1, phi2,expl, p, pbest[pi], gbest, numStates, data)
            
            if p.getScore() > pbest[pi].getScore():
                pbest[pi] = deepcopy(p)
                p.setPBestDist(list())
                if pbest[pi].getScore() > gbest.getScore():
                    gbest = deepcopy(pbest[pi])
                    for i in particles:
                        i.setGBestDist(calculateDistance(gbest, i))
        iteration += 1
    for q in range(len(gbest.adjMat)):
        for r in range(len(gbest.adjMat)):
            if gbest.adjMat[q][r] == 1 and gbest.adjMat[r][q] == 1:
                rand = random.random()
                if rand >= 0.5:
                    gbest.adjMat[q][r] = 0
                else:
                    gbest.adjMat[r][q] = 0
                
    return gbest
    
def insertU(x, y, particle, pbest, gbest, numStates, data):
    nx = findNeighbors(x, particle)
    ny = findNeighbors(y, particle)
    nxy = findSharedNeighbors(nx, ny)
    yPi = findParents(y, particle)
    xPi = findParents(x, particle)
    if undirPathValidityCheck(x, y, nxy, deepcopy(particle.chainMat)) and parentsEqualValidityCheck(xPi, yPi):
        nxy = appendNoDrama(nxy, yPi)
        adding = deepcopy(nxy)
        adding = appendNoDrama(adding, [deepcopy(x)])
        score = particle.getScore()
        score = score + calcNodeScore(y,adding, numStates, data) - calcNodeScore(y,nxy, numStates, data)
        particle.setScore(score)
        particle.adjMat[x][y] = 1
        particle.adjMat[y][x] = 1
        particle.chainMat[x][y] = 1
        particle.chainMat[y][x] = 1
        dp = particle.getPBestDist()
        newdp = updateDistance(x, y, particle, pbest, dp)
        particle.setPBestDist(newdp)
        dg = particle.getGBestDist()
        newdg = updateDistance(x, y, particle, gbest, dg)
        particle.setPBestDist(newdg)
    #need to adjust distance
    return particle

def insertD(x, y, particle, pbest, gbest, numStates, data):
    xPi = findParents(x, particle)
    yPi = findParents(y, particle)
    omega = findOmega(xPi, yPi)
    if insertDFirstValidityCheck(x, y, omega, deepcopy(particle.adjMat)) and nxyCliqueValidityCheck(omega, deepcopy(particle.adjMat)) and not parentsEqualValidityCheck(xPi, yPi):
        newyPi = deepcopy(yPi)
        newyPi = appendNoDrama(newyPi, [x])
        ny = findNeighbors(y, particle)
        newOmega = deepcopy(omega)
        newOmega = appendNoDrama(newOmega, newyPi)
        omega = appendNoDrama(omega, yPi)
        score = particle.getScore()
        score = score + calcNodeScore(y,newOmega, numStates, data) - calcNodeScore(y,omega, numStates, data)
        particle.setScore(score)
        particle.adjMat[x][y] = 1
        particle.adjMat[y][x] = 0
        particle.chainMat[x][y] = 0
        particle.chainMat[y][x] = 0
        #need to adjust distance
        dp = particle.getPBestDist()
        newdp = updateDistance(x, y, particle, pbest, dp)
        particle.setPBestDist(newdp)
        dg = particle.getGBestDist()
        newdg = updateDistance(x, y, particle, gbest, dg)
        particle.setPBestDist(newdg)
    return particle

def deleteD(x, y, particle, pbest, gbest, numStates, data):
    yPi = findParents(y, particle)
    ny = findNeighbors(y, particle)
    if nxyCliqueValidityCheck(ny, deepcopy(particle.adjMat)):
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
        particle.adjMat[y][x] = 0
        particle.chainMat[x][y] = 0
        particle.chainMat[y][x] = 0
        #need to adjust distance
        dp = particle.getPBestDist()
        newdp = updateDistance(x, y, particle, pbest, dp)
        particle.setPBestDist(newdp)
        dg = particle.getGBestDist()
        newdg = updateDistance(x, y, particle, gbest, dg)
        particle.setPBestDist(newdg)

    return particle

def reverseD(x, y, particle, pbest, gbest, numStates, data):
    yPi = findParents(y, particle)
    xPi = findParents(x, particle)
    nx = findNeighbors(x, particle)
    ny = findNeighbors(y, particle)
    omega = findOmega(yPi,nx)
    if reverseDFirstValidityCheck(x,y, omega, ny, deepcopy(particle.adjMat)) and nxyCliqueValidityCheck(omega, deepcopy(particle.adjMat)):
        newyPi = deepcopy(yPi)
        if x in newyPi:
            newyPi.remove(x)
        newxPi = deepcopy(xPi)
        newxPi = appendNoDrama(newxPi, [y])
        score = particle.getScore()
        score = score + calcNodeScore(y,newyPi, numStates, data) + calcNodeScore(x,appendNoDrama(newxPi, omega), numStates, data) - calcNodeScore(y,yPi, numStates, data) + calcNodeScore(x,appendNoDrama(xPi, omega), numStates, data)
        particle.setScore(score)
        particle.adjMat[x][y] = 0
        particle.adjMat[y][x] = 0
        particle.chainMat[x][y] = 0
        particle.chainMat[y][x] = 0
        #need to adjust distance
        dp = particle.getPBestDist()
        newdp = updateDistance(x, y, particle, pbest, dp)
        particle.setPBestDist(newdp)
        dg = particle.getGBestDist()
        newdg = updateDistance(x, y, particle, gbest, dg)
        particle.setPBestDist(newdg)
    return particle

def deleteU(x, y, particle, pbest, gbest, numStates, data):
    nx = findNeighbors(x, particle)
    ny = findNeighbors(y, particle)
    nxy = findSharedNeighbors(nx, ny)
    if nxyCliqueValidityCheck(nxy, deepcopy(particle.adjMat)):
        yPi = findParents(y, particle)
        nxy = appendNoDrama(nxy, yPi)
        removing = deepcopy(nxy)
        removing = appendNoDrama(removing, [x])
        score = particle.getScore()
        score = score + calcNodeScore(y,nxy, numStates, data) - calcNodeScore(y,removing, numStates, data)
        particle.setScore(score)
        particle.adjMat[x][y] = 0
        particle.adjMat[y][x] = 0
        particle.chainMat[x][y] = 0
        particle.chainMat[y][x] = 0
        #need to adjust distance
        dp = particle.getPBestDist()
        newdp = updateDistance(x, y, particle, pbest, dp)
        particle.setPBestDist(newdp)
        dg = particle.getGBestDist()
        newdg = updateDistance(x, y, particle, gbest, dg)
        particle.setPBestDist(newdg)
    return particle

def makeV(x, y, z, particle, pbest, gbest, numStates, data):
    nx = findNeighbors(x, particle)
    ny = findNeighbors(y, particle)
    nxy = findSharedNeighbors(nx, ny)

    if undirPathValidityCheck(x,y,nxy, deepcopy(particle.chainMat)):
        yPi = findParents(y, particle)
        zPi = findParents(z, particle)

        newzPi = deepcopy(zPi)
        newzPi = appendNoDrama(newzPi, [y])

        newnxy1 = deepcopy(nxy)
        newnxy1 = appendNoDrama(newnxy1, [x])
        if z in newnxy1:
            newnxy1.remove(z)
        
        newnxy2 = deepcopy(nxy)
        if z in newnxy2:
            newnxy2.remove(z)

        last = deepcopy(yPi)
        last = appendNoDrama(last, nxy)

        score = particle.getScore()
        score=score+calcNodeScore(z,appendNoDrama(newzPi,newnxy1),numStates,data)+calcNodeScore(y,appendNoDrama(yPi,newnxy2),numStates,data)-calcNodeScore(z,appendNoDrama(zPi,newnxy1),numStates,data)+calcNodeScore(y,last, numStates,data)

        particle.setScore(score)
        particle.adjMat[x][z] = 1
        particle.adjMat[z][x] = 0
        particle.adjMat[y][z] = 1
        particle.adjMat[z][y] = 0
        particle.chainMat[x][z] = 0
        particle.chainMat[y][z] = 0
        particle.chainMat[z][x] = 0
        particle.chainMat[z][y] = 0
        #need to adjust distance
        dp = particle.getPBestDist()
        newdp = updateDistance(x, z, particle, pbest, dp)
        particle.setPBestDist(newdp)
        dg = particle.getGBestDist()
        newdg = updateDistance(x, z, particle, gbest, dg)
        particle.setPBestDist(newdg)
        dp = particle.getPBestDist()
        newdp = updateDistance(y, z, particle, pbest, dp)
        particle.setPBestDist(newdp)
        dg = particle.getGBestDist()
        newdg = updateDistance(y, z, particle, gbest, dg)
        particle.setPBestDist(newdg)
    else:
        insertD(x, z, particle, pbest, gbest, numbStates, data)
    
    return particle

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
                sharedN.append(xNeighborSet[i])
    return sharedN

def findOmega(xParentsSet, yNeighborSet):
    bigOmega = list()
    for i in range(len(xParentsSet)):
        for j in range(len(yNeighborSet)):
            if xParentsSet[i] == yNeighborSet[j]:
                bigOmega.append(yNeighborSet[j])
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

def undirPathValidityCheck(x, y, Nxy, chainMat):
    searching = True
    visitedNodes = list()
    while searching:
        xtemp = deepcopy(x)
        S = list()
        S.append(xtemp)
        visitedNodes.append(xtemp)
        visitedEdges = list()
        while len(S) > 0:
            v = S.pop()
            if v == y:
                if y not in visitedNodes:
                    visitedNodes.append(y)
                #check that visitedEdges contains at least one pair of edges (i, j), (j, k) such that j in Nxy
                inNxy = False
                for (i, j) in visitedEdges:
                    for k in range(len(chainMat)):
                        if i != k and j != k:
                            if (j,k) in visitedEdges or (k, j) in visitedEdges:
                                if j in Nxy:
                                    inNxy = True
                                    chainMat[i][j] = 0
                                    chainMat[j][i] = 0
                                    chainMat[j][k] = 0
                                    chainMat[k][j] = 0
                                    break
                    if inNxy:
                        break
                if not Nxy:
                    return False
                else:
                    break
            else:
                if v not in visitedNodes:
                    visitedNodes.append(v)
                for node in range(len(chainMat)):
                    if chainMat[v][node] == 1:
                        if(v, node) not in visitedEdges and (node, v) not in visitedEdges:
                            visitedEdges.append((v,node))
        if y not in visitedNodes:
            searching = False
    return True

def parentsEqualValidityCheck(xPi, yPi):
    if len(xPi) == len(yPi):
        sharedParents = findSharedNeighbors(xPi, yPi)
        if len(sharedParents) == len(xPi) and len(sharedParents) == len(yPi):
            return True
        else:
            return False
    else:
        return False

def nxyCliqueValidityCheck(Nxy, adjMat):
    n1 = len(Nxy)
    count = 0
    for node1 in Nxy:
        for node2 in Nxy:
            if node1 != node2:
                if adjMat[node1][node2] == 1:
                    count += 1
    n = n1 * (n1-1)
    if count == n:
        return True
    #will take Nxy or OmegaXY
    return False

def insertDFirstValidityCheck(x, y, omegaXY, adjMat):
    searching = True
    visitedNodes = list()
    while searching:
        xtemp = deepcopy(x)
        S = list()
        S.append(xtemp)
        visitedNodes.append(xtemp)
        visitedEdges = list()
        while len(S) > 0:
            v = S.pop()
            if v == y:
                if y not in visitedNodes:
                    visitedNodes.append(y)
                #check that visitedEdges contains at least one pair of edges (i, j), (j, k) such that j in Nxy
                inNxy = False
                for (i, j) in visitedEdges:
                    for k in range(len(adjMat)):
                        if i != k and j != k:
                            if (j,k) in visitedEdges or (k, j) in visitedEdges:
                                if j in Nxy:
                                    inNxy = True
                                    adjMat[i][j] = 0
                                    adjMat[j][i] = 0
                                    adjMat[j][k] = 0
                                    adjMat[k][j] = 0
                                    break
                    if inNxy:
                        break
                if not Nxy:
                    return False
                else:
                    break
            else:
                if v not in visitedNodes:
                    visitedNodes.append(v)
                for node in range(len(adjMat)):
                    if adjMat[v][node] == 1:
                        if(v, node) not in visitedEdges and (node, v) not in visitedEdges:
                            visitedEdges.append((v,node))
        if y not in visitedNodes:
            searching = False
    return True

def reverseDFirstValidityCheck(x, y, omegaXY, Ny, adjMat):
    Nxy = deepcopy(omegaXY)
    Nxy = appendNoDrama(Nxy, Ny)
    searching = True
    visitedNodes = list()
    if adjMat[x][y] == 1 or adjMat[y][x] == 1:
        adjMat[x][y] = 0
        adjMat[y][x] = 0
    while searching:
        xtemp = deepcopy(x)
        S = list()
        S.append(xtemp)
        visitedNodes.append(xtemp)
        visitedEdges = list()
        while len(S) > 0:
            v = S.pop()
            if v == y:
                if y not in visitedNodes:
                    visitedNodes.append(y)
                #check that visitedEdges contains at least one pair of edges (i, j), (j, k) such that j in Nxy
                inNxy = False
                for (i, j) in visitedEdges:
                    for k in range(len(adjMat)):
                        if i != k and j != k:
                            if (j,k) in visitedEdges or (k, j) in visitedEdges:
                                if j in Nxy:
                                    inNxy = True
                                    adjMat[i][j] = 0
                                    adjMat[j][i] = 0
                                    adjMat[j][k] = 0
                                    adjMat[k][j] = 0
                                    break
                    if inNxy:
                        break
                if not Nxy:
                    return False
                else:
                    break
            else:
                if v not in visitedNodes:
                    visitedNodes.append(v)
                for node in range(len(adjMat)):
                    if adjMat[v][node] == 1:
                        if(v, node) not in visitedEdges and (node, v) not in visitedEdges:
                            visitedEdges.append((v,node))
        if y not in visitedNodes:
            searching = False
    return True

def calculateDistance(best, particle):
    distance = list()
    for i in range(len(particle.adjMat)):
        for j in range(len(particle.adjMat[0])):
            if best.adjMat[i][j] != particle.adjMat[i][j]:
                if (i, j) not in distance and (j,i) not in distance:
                    distance.append((i,j))
    return distance

def updateDistance(x, y, particle, best, distance):
    if (x,y) in distance or (y,x) in distance:
        if particle.adjMat[x][y] == best.adjMat[x][y] and particle.adjMat[y][x] == best.adjMat[y][x]:
            try:
                ind = distance.index((x,y))
            except Exception:
                ind = distance.index((y,x))
            del(distance[ind])
        #determine if bestxy and particlexy is same
        #if is same
            #subtract (x,y) from distance
    else:
        if particle.adjMat[x][y] != best.adjMat[x][y] or particle.adjMat[y][x] != best.adjMat[y][x]:
            distance.append((x,y))
        #determine if bestxy and particlexy is same
        #if is not same
            #add (x,y) to distance
    return distance

def updatePosition(phi1, phi2, expl, p, pbest, gbest, numStates, data):
    count = 0
    for (node1, node2) in p.pbestDistance:
        r1 = random.random()
        if r1 <= phi1:
            p = performUpdates(expl, p, node1, node2, pbest, pbest, gbest, numStates, data)
        else:
            pass
    for (node1, node2) in p.gbestDistance:
        r2 = random.random()
        if r2 <= phi2:
            p = performUpdates(expl, p, node1, node2, gbest, pbest, gbest, numStates, data)
        else:
            pass
    return p
        

def performUpdates(expl, p, node1, node2, best, pbest, gbest, numStates, data):
    if p.adjMat[node1][node2] == 0 and p.adjMat[node2][node1] == 0: #no edge
        if best.adjMat[node1][node2] == 1 and p.adjMat[node2][node1] == 1:
            r1 = random.random()
            if r1 >= expl:
                p = insertU(node1, node2, p, pbest, gbest, numStates, data)
                
            else:
                p = insertD(node1, node2, p,pbest, gbest,  numStates, data)
        elif best.adjMat[node1][node2] == 1 and best.adjMat[node2][node1] == 0:
            r1 = random.random()
            if r1 >= expl:
                p = insertD(node2, node1, p,pbest, gbest,  numStates, data)
                
            else:
                r1 = random.random()
                if r1 >= expl:
                    p = insertD(node1, node2, p,pbest, gbest,  numStates, data)
                    
                else:
                    p = insertU(node1, node2, p, pbest, gbest, numStates, data)
        elif best.adjMat[node1][node2] == 0 and best.adjMat[node2][node1] == 1:
            r1 = random.random()
            if r1 >= expl:
                p = insertD(node1, node2, p,pbest, gbest,  numStates, data)
                
            else:
                r1 = random.random()
                if r1 >= expl:
                    p = insertD(node2, node1, p,pbest, gbest,  numStates, data)
                    
                else:
                    p = insertU(node1, node2, p, pbest, gbest, numStates, data)
                
            
    elif p.adjMat[node1][node2] == 1 and p.adjMat[node2][node1] == 0: #directed edge
        r1 = random.random()
        if r1 >= expl:
            p = deleteD(node1, node2, p, pbest, gbest, numStates, data)
            
        else:
            p = reverseD(node1, node2, p, pbest, gbest,  numStates, data)
            
    elif p.adjMat[node2][node1] == 1 and p.adjMat[node1][node2] == 0: #directed edge other direction
        r1 = random.random()
        if r1 >= expl:
            p = deleteD(node2, node1, p, pbest, gbest, numStates, data)
            
        else:
            p = reverseD(node2, node1, p, pbest, gbest, numStates, data)
            
    else:                                                           #find potential V structure
        
        madeChange = False
        for el in range(len(p.chainMat)):
            for em in range(len(p.chainMat)):
                if p.chainMat[el][em] == 1:
                    for en in range(len(p.chainMat)):
                        if p.chainMat[em][en] == 1 and p.chainMat[el][en] == 0:
                            
                            madeChange = True
                            r1 = random.random()
                            if r1 >= expl:
                                r2 = random.random()
                                if r2 >= expl:
                                    p = deleteU(el, em, p, pbest, gbest, numStates, data)
                                else:
                                    p = deleteU(em, en, p, pbest, gbest, numStates, data)
                                
                            else:
                                p = makeV(el, em, en, p, pbest, gbest, numStates, data)
                                
                        else:
                            r1 = random.random()
                            if r1 >= expl:
                                madeChange = True
                                p = deleteU(el, em, p, pbest, gbest, numStates, data)
                                
                        if madeChange:
                            break
                if madeChange:
                    break
            if madeChange:
                break
    return p

def calcNodeScore(node, parents, numStates, data):
    nt = 10
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
    d = Decimal(0.09 ** ((ri-1)*qi))
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
    
    particleList = list()
    for i in range(numParticles):
        particleList.append(Particle(numNodes))
    for p in particleList:
        r = random.randint(numNodes, 2*numNodes)
        for it in range(r):
           
            node1 = random.randint(0, numNodes-1)
            node2 = random.randint(0, numNodes-1)
            while node1 == node2:
                node2 = random.randint(0, numNodes-1)
            
            if p.adjMat[node1][node2] == 0 and p.adjMat[node2][node1] == 0: #no edge
                r1 = random.random()
                if r1 >= 0.5:
                    p = insertU(node1, node2, p, p, p, numStates, data)
                    
                else:
                    p = insertD(node1, node2, p,p, p,  numStates, data)
                    
            elif p.adjMat[node1][node2] == 1 and p.adjMat[node2][node1] == 0: #directed edge
                r1 = random.random()
                if r1 >= 0.5:
                    p = deleteD(node1, node2, p, p, p, numStates, data)
                    
                else:
                    p = reverseD(node1, node2, p, p, p,  numStates, data)
                    
            elif p.adjMat[node2][node1] == 1 and p.adjMat[node1][node2] == 0: #directed edge other direction
                r1 = random.random()
                if r1 >= 0.5:
                    p = deleteD(node2, node1, p, p, p, numStates, data)
                    
                else:
                    p = reverseD(node2, node1, p, p, p, numStates, data)
                    
            else:                                                           #find potential V structure
                
                madeChange = False
                for el in range(len(p.chainMat)):
                    for em in range(len(p.chainMat)):
                        if p.chainMat[el][em] == 1:
                            for en in range(len(p.chainMat)):
                                if p.chainMat[em][en] == 1 and p.chainMat[el][en] == 0:
                                    
                                    madeChange = True
                                    r1 = random.random()
                                    if r1 < 0.5:
                                        r2 = random.random()
                                        if r2 >= 0.5:
                                            p = deleteU(el, em, p, p, p, numStates, data)
                                        else:
                                            p = deleteU(em, en, p, p, p, numStates, data)
                                        
                                    else:
                                        p = makeV(el, em, en, p,p,p, numStates, data)
                                        
                                else:
                                    r1 = random.random()
                                    if r1 >= 0.9:
                                        madeChange = True
                                        p = deleteU(el, em, p, p, p, numStates, data)
                                        
                                if madeChange:
                                    break
                        if madeChange:
                            break
                    if madeChange:
                        break
        score = calculateScore(p, numStates, data)
        
        p.setScore(score)
    return particleList 

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

def compareGraphs(particle, graphDict):
    if (len(graphDict) != particle.numNodes):
        return False
    #first create an array with the number of elements
    nodeCounter = 0
    for i in graphDict:
        basicAdjacencyArray = []
        for j in graphDict:
            basicAdjacencyArray.append(0) 
        for parents in graphDict[i].tablegivens:
            if parents in graphDict:
                basicAdjacencyArray[graphDict[parents].number] = 1
        if basicAdjacencyArray != particle.adjMat[nodeCounter]:
            return False
        nodeCounter = nodeCounter + 1
    return True

def probTables(nodes,states,massiveData,massiveDictionary): #say nodes are A B C D and you want them to be in +a -b +c -d or something like that
    # assuming both are being passsed as arrays and in order so
    #probTables([A,B,C,D], [+a,-b,+c,-d])
    #assuming that both arrays elements have been passed as strings "A" "B" etc
    #massiveData are the samples that have been generated already
    positions = []
    validSample = 0
    counter = 0
    for i in nodes:
        if i in massiveDictionary:
            positions.append(massiveDictionary[i].number) #append the index on A,B etc in massiveDictionary to positions array
    for i in massiveData:
        k = 0
        validSample = 1
        while(k<len(positions)):
            if(i[positions[k]] != states[k]):
                validSample = 0
                break
            k = k+1
        if validSample == 1:
            counter = counter + 1
    return float(counter/len(massiveData))


def main():
    p = parser.Parser()
    (massiveDictionary,adjacencyDictionary) = p.fileparser('asia.bif')
    massiveData = p.dataGeneration(massiveDictionary,1000) #specify desired number of samples
    hcAlgo = hill_climb.HC()
    edges = hcAlgo.hillclimb(len(massiveData[0]), massiveData, massiveDictionary)
    print(edges)
    gbest = ecPSO(0.5, 0.5, 0.9, 10,100, len(massiveData[0]), massiveData, massiveDictionary)
    
    
    
    for line in gbest.adjMat:
        print(line)
    #print(gbest)
    
if __name__ == "__main__": main()
    
