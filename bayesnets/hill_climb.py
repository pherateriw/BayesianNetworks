import bif_parser
from sys import maxsize
from collections import OrderedDict

def run():
    m = bif_parser.Parser() #instantiate parser
    tables = m.createTable('alarm.bif') #call parsing function
    varlist = list(tables.keys()) #determine the list of variables
    tablist = list(tables.values())
    print(varlist)
    for i in tablist:
        print()
        #print(tablist[i[0]])
    edges = list()
    score = -maxsize
    maxscore = score + 1
    while(score > maxscore):
        maxscore = score
        for x in varlist :
            for y in varlist :
                print(tables[y])
                    
    

if __name__ == '__main__':
    run()
