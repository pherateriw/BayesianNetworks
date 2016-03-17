'''
Created on Mar 17, 2016

@author: Jani
'''
class Node(object):
    '''
    Each Node stores a node name, a set of states, a conditional probability table and the parents given in table
    '''


    def __init__(self, name, states, table, tablegivens ):
        '''
        Constructor
        '''
        self.name = name; #node name
        self.states = states; #tuple of states
        self.table = table; #dictionary of tuples
        self.tablegivens = tablegivens; #tuple of nodes from table
        