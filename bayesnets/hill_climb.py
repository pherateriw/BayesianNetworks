import bif_parser 
from collections import OrderedDict

def run():
    m = bif_parser.Parser()
    tables = m.createTable('alarm.bif')
    #print(tables)

if __name__ == '__main__':
    run()
