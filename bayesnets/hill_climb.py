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
    score = -maxsize
    maxscore = score -1
    while(score > maxscore):
        maxscore = score
        for x in tables:
            #tabx = tables[x].getTable()
            #print(tabx)
            #namex = tables[x].getName()
            #statesx = tables[x].getStates()
            #parentsx = tables[x].getTableGivens()
            #print()
            #print(namex)
            #print(tabx)
            #print(statesx)
            #print(parentsx)
            #for z in tabx:
                #print(z, " : ",  tabx[z])
            for y in tables:
                taby = tables[y].getTable()
                tabx = tables[x].getTable()
                if(x,y) in edges:
                    print((x,y))
                else:
                    print("not", (x,y))
                
                
                    
    

if __name__ == '__main__':
    run()
