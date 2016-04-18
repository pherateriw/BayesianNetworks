from particle import Particle

def psoE(numParticles, data):
    #import data
    particles = initParticles(numParticles)
    for 
    


def insertU(x, y, score, adjMat, chainMat, distance):
    pass

def insertD(x, y, score, adjMat, distance):
    pass

def deleteD(x, y, score, adjMat, distance):
    pass

def reverseD(x, y, score, adjMat, distance):
    pass

def deleteU(x, y, score, adjMat, chainMat, distance):
    pass

def makeV(x, y, z, score, adjMat, chainMat, distance):
    pass

def calculateScore():
    pass

def updateScore():
    pass

def calculateDistance():
    pass

def updateDistance():
    pass

def initParticles(numParticles):
    particleList = [Particle(numParticle)]*numParticles
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
        #find best particle and set to gbest
        pass
    return particleList #also how to store pbest and gbest?
    
