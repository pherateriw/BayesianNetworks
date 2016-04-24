from sys import maxsize

class Particle:
    def __init__(self, numNodes):
        self.numNodes = numNodes
        self.adjMat = list()
        for i in range(numNodes):
            minilist = list()
            for j in range(numNodes):
                minilist.append(0)
            self.adjMat.append(minilist)
        self.chainMat = list()
        for i in range(numNodes):
            minilist2 = list()
            for j in range(numNodes):
                minilist2.append(0)
            self.chainMat.append(minilist2)
        self.pbestDistance = list()
        self.gbestDistance = list()
        self.velocity = {}
        self.score = -maxsize
        

    def getData(self):
        return self.data

    def getAdjMat(self):
        return self.adjMat

    def getChainMat(self):
        return self.chainMat

    def setAdjMat(self, adjMat):
        self.adjMat = adjMat

    def setChainMat(self, chainMat):
        self.chainMat = chainMat

    def getPBestDist(self):
        return self.pbestDistance

    def getGBestDist(self):
        return self.gbestDistance

    def setPBestDist(self, distance):
        self.pbestDistance = distance

    def setGBestDist(self, distance):
        self.gbestDistance = distance

    def getVelocity(self):
        return self.velocity

    def setVelocity(self, velocity):
        self.velocity = velocity

    def getScore(self):
        return self.score

    def setScore(self, score):
        self.score = score

