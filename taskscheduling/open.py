import heapq
from collections import deque

from problem import *

class sNodeWrapper:
    ''' Wrapper around sNode that implements various comparison operators for 
        ordering the nodes on a priority heap'''
    def __init__(self, node):
        self.node = node

    def __lt__(self, other):
        '''For astar and best first we use a priority queue for the
           OPEN set. This queue stores search nodes waiting to be
           expanded. Thus we need to define a node1 < node2 function
           by defining the __lt__ function. Dependent on the type of
           search this comparison function compares the h-value, the
           g-value or the f-value of the nodes. Note for the f-value
           we wish to break ties by letting node1 < node2 if they both
           have identical f-values but if node1 has a GREATER g
           value. This means that we expand nodes along deeper paths
           first causing the search to proceed directly to the goal'''
        return True # No explicit ordering on the nodes (BFS/DFS)

class sNodeWrapperH(sNodeWrapper):
    def __lt__(self, other):
        ''' Best-first search '''
        return self.node.hval < other.node.hval

class sNodeWrapperHG(sNodeWrapper):
    def __lt__(self, other):
        ''' A* search '''
        selfHG  = self.node.gval + self.node.hval
        otherHG = other.node.gval + other.node.hval

        if selfHG == otherHG:
            # break ties by greatest gval
            return self.node.gval > other.node.gval
        return selfHG < otherHG

class Open:
    '''Open objects hold the search frontier---the set of unexpanded
       nodes. Depending on the search strategy used we want to extract
       nodes from this set in different orders, so derive the object's
       functions to operate as needed by the particular search
       strategy'''

    def __init__(self):
        self.open = []
        self.nodes_expanded = 0 # Number of nodes extracted

    def clear(self):
        ''' Clear nodes from open list '''
        self.open.clear()
        self.nodes_expanded = 0

    def insert(self, node):
        '''Input a search node into the open list'''
        pass

    def extend(self, nodes):
        '''Inputs a list of search nodes into the open list.
           These are assumed to be from a nodes' successor function.
           (i.e. all same depth level and parent)'''
        for n in nodes:
            self.insert(n)

    def extract(self):
        '''Extract a search node from the open list'''
        pass

    def empty(self): 
        return not self.open

    def print_type(self):
        return "abstract (should not be instantiated)"

    def print_open(self):
        print("{", end=' ')
        if self.open:
            for nd in self.open:
                print("   " + str(nd.node), end=' ')
        print("}")


class OpenDFS(Open):
    '''Open list used in DFS search (open list is a stack)'''

    def insert(self, node):
        self.open.append(sNodeWrapper(node))

    def extract(self):
        self.nodes_expanded += 1
        return self.open.pop().node

    def print_type(self):
        return "depth_first"

class OpenBFS(Open):
    '''Open list used in BFS search (open list is a queue)'''

    def __init__(self):
        Open.__init__(self)
        self.open = deque() # Use a faster deque 

    def insert(self, node):
        self.open.append(sNodeWrapper(node))

    def extract(self):
        self.nodes_expanded += 1
        return self.open.popleft().node

    def print_type(self):
        return "breadth_first"

class OpenBF(Open):
    '''Open list used in best-first search (open list is a priority queue sorted by H)'''

    def insert(self, node):
        heapq.heappush(self.open, sNodeWrapperH(node))

    def extract(self):
        self.nodes_expanded += 1
        return heapq.heappop(self.open).node

    def print_type(self):
        return "best_first"

class OpenAStar(Open):
    '''Open list used in A* search (open list is a priority queue sorted by F=G+H)'''

    def insert(self, node):
        heapq.heappush(self.open, sNodeWrapperHG(node))

    def extract(self):
        self.nodes_expanded += 1
        return heapq.heappop(self.open).node

    def print_type(self):
        return "astar"

class OpenIDAStar(Open):
    '''Open list used in IDA* search (open list is a stack where nodes are not inserted 
       if their F=G+H values exceed some bound'''

    def __init__(self, bound):
        Open.__init__(self)
        self.bound = bound # F-bound
        self.min   = -1    # Minimum fval that is larger than self.bound

    def insert(self, node):
        fval = node.gval + node.hval
        # If the fval is greater than the bound, do not add it to the open list
        if fval > self.bound:
            # Is this the smallest fval we've seen that is larger than the bound?
            if (self.min == -1) or (fval < self.min):
                # Store it, will be used on the next IDA* pass if necessary
                self.min = fval
        else:
            self.open.append(sNodeWrapper(node))

    def extract(self):
        self.nodes_expanded += 1
        return self.open.pop().node

    def print_type(self):
        return "idastar"
