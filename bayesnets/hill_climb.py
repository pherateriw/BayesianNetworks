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
    #print(tables['KINKEDTUBE'].getTable())
    edges = list()
    edgesprime = list()
    score = -maxsize
    maxscore = score -1
    newscore = maxscore
    #while(score > maxscore):
    maxscore = score
    for x in tables:
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
                        
def bicScore(edgeList, probTables):
    return 0

def recalculateProbTables(edgesList, probTables, tablesPrime):
    print('recalculating...')
    for (x,y) in edgesList:
        z = probTables[x].getTableGivens()
        if y in z:
            i = z.index(y)
            olist = probTables[x].getTable()
            statelist = probTables[y].getStates()
            
            print(olist)
            #find the probability in the table
            #calculate
        else:
            #print(z)
            pass
            #calculate the probability and create the table
    
        
    return probTables
                        
                
                
                    
    

if __name__ == '__main__':
    run()
