from particle import Particle
import bif_parser as parser
from sys import maxsize

def ecPSO(numParticles, numNodes, data):
    #import data
    particles = initParticles(numParticles, numNodes)
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

def calculateScore(particle):
    """returns the BDeu criterion """
    for node in len(particle.adjMat):
        pass

def calculateDistance():
    pass

def updateDistance():
    pass

def updateVelocity(velocity):
    return velocity

def updatePosition(particle):
    #call update score
    return particle

def initParticles(numParticles, numNodes):
    particleList = [Particle(numNodes)]*numNodes
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
    
def main():
    p = parser.Parser()
    (massiveDictionary,adjacencyDictionary) = p.fileparser('asia.bif')
    massiveData = p.dataGeneration(massiveDictionary,200) #specify desired number of samples
    ecPSO(5,len(massiveData[0]), massiveData)
    #print(massiveData)
    #JANETTE#
    #adjacencyDict is the one you are prolly interested in
    #instead of 50 replace it with how many samples you want
    
if __name__ == "__main__": main()
