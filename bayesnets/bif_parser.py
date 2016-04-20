from collections import OrderedDict
import random

def returnTypeIndex(array, probability):
    i = 0;
    while(i<len(array)):
        if(probability <= array[i]):
            return i
        else:
            probability = probability - array[i]
        i = i+1
    if(i == len(array)):
        return len(array)-1

class Node:
    def __init__(self, name, states, tablegivens, table, number):
        self.name = name
        self.states = states
        self.table = table
        self.tablegivens = tablegivens
        self.number = number
    def getName(self):
        return self.name
    def getStates(self):
        return self.states
    def getTable(self):
        return self.table
    def getTableGivens(self):
        return self.tablegivens

class Parser:
    def __init__(self):
       self.data = []
        
    def fileparser(self, filename):       
        dict = OrderedDict() ############
        matrixDict = OrderedDict()
        stateArray = [] #stores all states
        dataParents = []
        probDict = OrderedDict() #########
        probValues = []
        tableDict = OrderedDict()
        arraycounter = 0
        conditionNames = [] #used for storing the names of conditions in order. For the BOTTOM part of the file where values are listed. 
        f = open(filename, 'r') ##'asia.bif'
        for line in f:
            #print(line)
            a = line.replace(",", " ").split()
            if(a[0] == "variable"):
                z = f.readline().replace(",", " ").split()
                i = 6; #this I is used for traversing over the above split line
                stateArray = []
                while(i < len(z)-1):
                    stateArray.append(z[i])
                    i = i+1
                #print(nodeName)
                #print(stateArray)
                dict[a[1]] = Node(a[1],stateArray,3,4,arraycounter) #here a node has been created with name and its states
                # parental information and probability will be updated down
                arraycounter = arraycounter + 1
            if(a[0] == "probability"):
               # print(a)
                #dataParents = []
                if(a[3] == "|"):
                    counter = 1
                    dataParents = a[4:len(a)-2]
                    dict[a[2]].tablegivens = dataParents
                    for i in dataParents:
                        counter = counter * len(dict[i].states)
                    i = 0
                    tableDict = OrderedDict()
                    while(i<counter):
                        z = f.readline().replace(",", " ").replace(";", " ").replace("(", " ").replace(")", " ").split()
                        #print(z)
                        conditionNames = []
                        probValues = []
                        for x in z:
                            try:
                                probValues.append(float(x))
                            except ValueError:
                                conditionNames.append(x)
                        #print(conditionNames)
                        #print(probValues)
                        tableDict[tuple(conditionNames)] = probValues
                        i = i+1
                    dict[a[2]].table = tableDict
                    #print(tableDict) ###
                    #print(dataParents)
                else:
                    probDict = OrderedDict()
                    probValues = []
                    dataParents = [""] #parents are being set to blank string
                    dict[a[2]].tablegivens = dataParents
                    z = f.readline().replace(",", " ").replace(";", " ").split()
                    probDict["independent"] = [float(z[1]),float(z[2])] #need to convert to number from string
                    #print(probDict["independent"])
                    dict[a[2]].table = probDict
        for i in dict:
            matrixDict[dict[i].name] = dict[i].tablegivens
        #for i in matrixDict:
        #    print(i, matrixDict[i])
        return (dict, matrixDict)
        
    def dataGeneration(self, dict, numberOfSamples):
        #need to generate random numbers between 0.01 and 0.99 use random.uniform(0.01,0.99)
        i = 0
        samplesCounter = 0
        numberOfSamplesNeeded = numberOfSamples
        generatedCompleteData = []
        while(samplesCounter<numberOfSamplesNeeded):
            i=0
            sampleRandoms = []
            generatedData = []
            while(i<len(dict)):
                sampleRandoms.append(round(random.uniform(0.01,0.99),2))#rounding to 2 decimal places
                generatedData.append(None)
                i=i+1
            #print(sampleRandoms)
            
            for i in dict:
                if(dict[i].tablegivens == [""]):
                    #print(dict[i].table)
                    probability =  sampleRandoms[dict[i].number] #probability generated is now associated with a node which has no parents
                    indexReturned = returnTypeIndex(dict[i].table["independent"], probability)
                    generatedData[dict[i].number] = dict[i].states[indexReturned]
                    #print(indexReturned, dict[i].states[indexReturned])
                    #print("true")
            #print(generatedData)
            
            parentCount = 1 #start with nodes which have only one parents and then go up
            continueLoop = 0
            
            while(None in generatedData):
                for i in dict :
                    continueLoop = 0
                    if((len(dict[i].tablegivens) ==  parentCount) and not("independent" in dict[i].table)): #need to make sure parents doesnt say independent
                        parentStates = []
                        for j in dict[i].tablegivens: #for every parent in tablegivens
                            #if(parentCount == 2):
                            #   print(j)
                            #print(j)
                            for k in dict:
                                if (dict[k].name == j):
                                    if(parentCount == 1):
                                        asdasd =  1
                                        #print(dict[k].name)
                                    indexOfParent = dict[k].number
                                    if(generatedData[indexOfParent] == None):
                                        continueLoop = 1
                                        break
                                    else:
                                        parentStates.append(generatedData[indexOfParent]) ##one parent doesnt mean that the parents data has been filled in 
                                    if(parentCount == 1):
                                        asdasd = 2
                                        #print(parentStates)
                            if continueLoop == 1:
                                break
                        for m in dict[i].table: #here m is a key which is a tuple
                            if(tuple(parentStates) == m):
                                probability = sampleRandoms[dict[i].number]
                                indexReturned = returnTypeIndex(dict[i].table[m], probability)
                                #print(indexReturned)
                                generatedData[dict[i].number] = dict[i].states[indexReturned]
                        #print(parentStates)
                #print(generatedData)
                parentCount = parentCount + 1
                if(parentCount == 1000): #if parents are 10 nodes go back to 1 node
                    parentCount = 1
            samplesCounter=samplesCounter+1
            generatedCompleteData.append(generatedData)
            #print(generatedData)
        #print(generatedCompleteData)
        return generatedCompleteData
        
def main():
    p = Parser()
    (massiveDictionary,adjacencyDictionary) = p.fileparser('alarm.bif')
    massiveData = p.dataGeneration(massiveDictionary,200) #specify desired number of samples
    print(massiveData)
    #JANETTE#
    #adjacencyDict is the one you are prolly interested in
    #instead of 50 replace it with how many samples you want
    
if __name__ == "__main__": main()

