from collections import OrderedDict
class Node:
    def __init__(self, name, states, tablegivens, table):
        self.name = name
        self.states = states
        self.table = table
        self.tablegivens = tablegivens
class Parser:
    def __init__(self):
       self.data = []
        
    def createTable(filename, stuff):
        dict = OrderedDict() ############
        stateArray = [] #stores all states
        dataParents = []
        probDict = OrderedDict() #########
        probValues = []
        tableDict = OrderedDict()
        conditionNames = [] #used for storing the names of conditions in order. For the BOTTOM part of the file where values are listed. 
        f = open('alarm.bif', 'r')
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
                dict[a[1]] = Node(a[1],stateArray,3,4) #here a node has been created with name and its states
                # parental information and probability will be updated down
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
                        print(z)
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
                    print(tableDict)
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
        #for i in dict:
            #print(dict[i].name)
        return tableDict
