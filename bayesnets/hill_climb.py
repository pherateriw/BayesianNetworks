import bif_parser
from sys import maxsize
from collections import OrderedDict

def run():
    m = bif_parser.Parser() #instantiate parser
    tables = m.createTable('alarm.bif') #call parsing function
    tablesprime = OrderedDict() #creat probability tables list
    varlist = list(tables.keys()) #determine the list of variables
    tablist = list(tables.values())
    edges = list() #create edge list
    edgesprime = list()
    score = -maxsize #set score to large negative value
    maxscore = score -1
    newscore = maxscore
    while(score > maxscore):
        maxscore = score
        for x in tables:
            #print(x, len(tables[x].getTableGivens()))
            for y in tables:
                if x != y:
                    taby = tables[y].getTable()
                    tabx = tables[x].getTable()
                
                    if(x,y) in edges:
                        #print((x,y))
                        #subtract edge
                        edgesprime.remove((x,y))
                        #recalculate probability tables and score
                        tablesPrime = recalculateProbTables(edgesprime, tables, tablesprime)
                        newscore = bicScore(edgesPrime, tablesPrime)
                        if newscore > score:
                            edges = edgesprime.deepcopy()
                            score = newscore
                            
                        #flip edge
                        edgesprime.remove((x,y))
                        edgesprime.append((y,x))
                        #recalculate probability tables and score
                        tablesPrime = recalculateProbTables(edgesprime, tables, tablesprime)
                        newscore = bicScore(edgesPrime, tablesPrime)
                        if newscore > score:
                            edges = edgesprime.deepcopy()
                            score = newscore
                    else:
                        #print(x,y)
                        #add edge
                        edgesprime.append((x,y))
                        #recalculate probability tables and score
                        tablesPrime = recalculateProbTables(edgesprime, tables, tablesprime)
                        newscore = bicScore(edgesPrime, tablesPrime)
                        if newscore > score:
                            edges = edgesprime.deepcopy()
                            score = newscore
                        
                        
def bicScore(edgeList, tablesPrime):
    return 0

def recalculateProbTables(edgesList, probTables, tablesPrime):
   
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
