

class Particle:
    def __init__(self, numNodes):
        self.adjMat = [[0]*numNodes]*numNodes
        self.chainMat = [[0]*numNodes]*numNodes
        self.pbestDistance = maxsize
        self.gbestDistance = maxsize
        self.velocity = {}
        self.score = 0
        

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

