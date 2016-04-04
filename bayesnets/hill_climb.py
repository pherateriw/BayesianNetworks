import bif_parser
from sys import maxsize
from collections import OrderedDict

def run():
    m = bif_parser.Parser() #instantiate parser
    tables = m.createTable('alarm.bif') #call parsing function
    tablesprime = OrderedDict()
    varlist = list(tables.keys()) #determine the list of variables
    tablist = list(tables.values())
    #print(varlist)
    print(tables['HYPOVOLEMIA'].getTableGivens())
    edges = list()
    edgesprime = list()
    score = -maxsize
    maxscore = score -1
    newscore = maxscore
    #while(score > maxscore):
    maxscore = score
    for x in tables:
        print(x, len(tables[x].getTableGivens()))
        for y in tables:
            if x != y:
                taby = tables[y].getTable()
                tabx = tables[x].getTable()
                
                if(x,y) in edges or (y,x) in edges:
                    #print((x,y))
                    #subtract edge
                    #recalculate probability tables and score
                    #flip edge
                    #recalculate probability tables and score
                    newscore = 0
                else:
                    #print(x,y)
                    #add edge
                    edgesprime.append((x,y))
                    tablesPrime = recalculateProbTables(edgesprime, tables, tablesprime)
                    #recalculate probability tables and score
                if newscore > score:
                    score = newscore
                        
def bicScore(edgeList, tablesPrime):
    return 0

def recalculateProbTables(edgesList, probTables, tablesPrime):
    #print('recalculating...')
    tablesPrime = OrderedDict()
    for (x,y) in edgesList:
        z = probTables[y].getTableGivens()
        yStates = probTables[y].getStates()
        yProb = probTables[y].getTable()
        substatelist = probTables[x].getStates()
        if x in z:
            if len(z) == 1:
                tablesPrime[y] = bif_parser.Node(y, yStates, z, yProb)
                #print(y, tablesPrime[y])
            elif len(z) >1:
                count  = 0
                for i in z:
                    if (i, y) in edgesList:
                        count += 1
                    else:
                        #want to remove i from z and i from table
                        iplace = z.index(i)
                        z.remove(i)
                        #print(y, len(yProb), yProb)
                        #should cycle through yprob,
                        for line in yProb:
                            #create partial tuples of yprob key with None instead of i states
                            tuplelen = len(line)
                            a = list(line)
                            a[iplace] = None
                            a = tuple(a)
                            #Find all partial tuples that match each other
                            tuplesmatch = GetTuples(yProb, a, tuplelen)
                            print(tuplesmatch)
                            a = list(a)
                            a.pop(iplace)
                            a = tuple(a)
                            #add the probabilities of the matching tuples
                            probability = []
                            for state in yStates:
                            
                            #Divide each probability by the number of matching partial tuples

                            #create a dictionary of a:probability
                if count == len(z):
                    tablesPrime[y] = bif_parser.Node(y, yStates, z, yProb)
                #i = z.index(y)
           
            
            #print(olist)
            #find the probability in the table
            #calculate
        else:
            if not z[0]:
               # print(z)
                #print(len(z))
                pass
            else:
                pass
            #print(z)
            #pass
            #calculate the probability and create the table
    
        
    return probTables
                        
def GetTuples(probTable, keyWords, tuplelen):
    tuples = []
    for k in probTable.keys():
        match = True
        for i in range(tuplelen):
            if keyWords[i] is not None and keyWords[i] != k[i]:
                match = False
                break
        if match is True:
            tuples.append(k)
    return tuples      
                    
    

if __name__ == '__main__':
    run()
