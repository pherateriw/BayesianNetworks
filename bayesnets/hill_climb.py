import bif_parser
from sys import maxsize
from collections import OrderedDict

def run():
    m = bif_parser.Parser() #instantiate parser
    tables = m.createTable('alarm.bif') #call parsing function
    varlist = list(tables.keys()) #determine the list of variables
    tablist = list(tables.values())
    #print(varlist)
    #print(tables['KINKEDTUBE'].getTable())
    edges = list()
    edgesprime = list()
    score = -maxsize
    maxscore = score -1
    while(score > maxscore):
        maxscore = score
        for x in tables:
            for y in tables:
                if x != y:
                    taby = tables[y].getTable()
                    tabx = tables[x].getTable()
                    if(x,y) in edges:
                        print((x,y))
                        #subtract edge
                        #recalculate probability tables and score
                        #flip edge
                        #recalculate probability tables and score
                        newscore = 0
                    else:
                        print(x,y)
                        #add edge
                        #recalculate probability tables and score
                    if newscore > score:
                        score = newscore
                        
def bifScore(edgeList, probTables):
    return 0

def recalculateProbTables(edgesList, probTables):
    return probTables
                        
                
                
                    
    

if __name__ == '__main__':
    run()
