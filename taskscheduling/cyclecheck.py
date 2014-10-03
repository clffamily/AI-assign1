from problem import *

'''Classes that handle cycle checking
   Null = no cycle checking
   Path = no cycles on paths to the initial state
   Full = never expand the same state twice'''

class CycleCheck:
    ''' Abstract base class (do not instantiate) '''
    def __init__(self):
        self.pruned_nodes = 0

    def prune(self, problem, node):
        '''Prune input state?'''
        pass

    def lazy_check(self, problem, node):
        '''In cycle checking, it might be the case that the same state
           has already been expanded with a lower g-value even if previously
           we decided not to prune this state. This does not happen with other
           cycle checking strategies, so return false'''
        return False

    def clear(self):
        self.pruned_nodes = 0

    def print_type(self):
        return "abstract (shouldn't be instantiated)"

    def print_debug(self):
        return ""

class NullCheck(CycleCheck):
    ''' No cycle checking '''

    def prune(self, problem, node):
        return False

    def print_type(self):
        return "no cycle checking"

class PathCheck(CycleCheck):
    ''' Path cycle checking '''

    def prune(self, problem, node):
        if node.has_path_cycle(problem):
            self.pruned_nodes += 1
            return True
        return False

    def print_type(self):
        return "path checking"

class FullCheck(CycleCheck):
    ''' Full cycle checking 
        Perform full cycle checking as follows
         a. check state before inserting into OPEN. If we had already reached
            the same state via a cheaper path, don't insert into OPEN.
            This is the function "prune"
         b. Sometimes we find a new cheaper path to a state (after the older
            more expensive path to the state has already been inserted.
            We deal with this lazily. We check states extracted from OPEN
            and if we have already expanded that state via a cheaper path
            we don't expand it. If we had expanded the state via a more
            expensive path, we re-expand it.
            This is the function "lazy_check"'''

    def __init__(self):
        CycleCheck.__init__(self)
        self.cc_dictionary = dict() # contains path cost of all states seen so far

    def prune(self, problem, node):
        hs = problem.hashable_state(node.state)
        # Prune state if it's in the dictionary with a larger path cost
        if (hs in self.cc_dictionary) and (node.gval > self.cc_dictionary[hs]):
            self.pruned_nodes += 1
            return True
        # else add the state and path cost to the dictionary
        self.cc_dictionary[hs] = node.gval
        return False

    def lazy_check(self, problem, node):
        hs = problem.hashable_state(node.state)
        # Prune state if it's in the dictionary with a larger path cost
        if (hs in self.cc_dictionary) and (node.gval > self.cc_dictionary[hs]):
            self.pruned_nodes += 1
            return True
        return False

    def clear(self):
        CycleCheck.clear(self)
        self.cc_dictionary = dict()

    def print_type(self):
        return "full cycle checking"

    def print_debug(self):
        print(self.cc_dictionary)

    def print_cc_debug(self, problem, node):
        hs = problem.hashable_state(node.state)
        print("CC_dict gval={}, node.gval={}".format(self.cc_dictionary[hs], node.gval))
