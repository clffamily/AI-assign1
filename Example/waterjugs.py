'''EXAMPLE STATESPACE WATERJUGS

States in the waterjugs problem can be represented by two integers, (gal3,gal4), where gal3 is the amount of water
in the 3 gallon jug, and gal4 is the amount of water in the 4 gallon jug.

'''

from problem import *

class WaterJugsState:

    def __init__(self, gal3, gal4):
        self.gal3 = gal3
        self.gal4 = gal4

    def __repr__(self):
        ret = "(3gal, 4gal) = ({},{})".format(self.gal3, self.gal4)
        return ret

class WaterJugs(Problem):
        
    def successors(self, state):
        """We have x actions, (1) empty the gal3, (2) fill the gal3,
        (3) empty the gal4, (4) fill the gal4 (5) pour the
        gal3-->gal4, (6) pour the gal4-->gal3.  all actions have cost
        1.  in computing the list of successor states, however, make
        sure we don't return a state equal to self as this is a null
        transtion."""

        States = list()
        if state.gal3 > 0 :
            States.append( ('Empty 3 Gallon', 1, WaterJugsState(0, state.gal4)) )
        if state.gal3 < 3 :
            States.append( ('Fill 3 Gallon', 1, WaterJugsState(3, state.gal4)) )
        if state.gal4 > 0 :
            States.append( ('Empty 4 Gallon', 1, WaterJugsState(state.gal3, 0)) )
        if state.gal4 < 4 :
            States.append( ('Fill 4 Gallon', 1, WaterJugsState(state.gal3, 4)) )
        if state.gal4 < 4 and state.gal3 > 0:
            maxpour = min( 4 - state.gal4, state.gal3 ) #at most can only fill up 4 gallon
            States.append( ('Pour 3 into 4', 1, WaterJugsState(state.gal3-maxpour, state.gal4+maxpour)) )
        if state.gal3 < 3 and state.gal4 > 0:
            maxpour = min( 3 - state.gal3, state.gal4 ) #at most can only fill up 3 gallon
            States.append( ('Pour 4 into 3', 1, WaterJugsState(state.gal3+maxpour, state.gal4-maxpour)) )
        return States

    def goal_check(self, state):
        '''test if the state is equal to the current goal,
        allow wild cards '*' in the goal state'''
        return ((self.goal.gal3 == '*' or
                 self.goal.gal3 == state.gal3) and
                (self.goal.gal4 == '*' or
                 self.goal.gal4 == state.gal4))

    def hashable_state(self, state):
        return (state.gal3, state.gal4)

def create_waterjugs_problem(init_gal3, init_gal4, goal_gal3, goal_gal4):
    return WaterJugs(WaterJugsState(init_gal3, init_gal4), WaterJugsState(goal_gal3, goal_gal4))
 
#Some auxillary heuristic functions 

def waterjugs_h_sum_function(problem, state):
    hval = 0
    if problem.goal.gal3 != '*':
        hval = hval + abs(problem.goal.gal3 - state.gal3)
    if problem.goal.gal4 != '*':
        hval = hval + abs(problem.goal.gal4 - state.gal4)
    return hval

def waterjugs_h_max_function(problem, state):
    hval = 0
    if problem.goal.gal3 != '*':
        hval = abs(problem.goal.gal3 - state.gal3)
    if problem.goal.gal4 != '*':
        hval = max(hval,abs(problem.goal.gal4 - state.gal4))
    return hval

def waterjugs_h_total_diff_function(problem, state):
    hval = 0
    if problem.goal.gal3 != '*':
        wsum = problem.goal.gal3
    if problem.goal.gal4 != '*':
        wsum = wsum + problem.goal.gal4
    return abs(state.gal3+state.gal4 - wsum)



# Some tests
if __name__ == "__main__":

    from search import *

    waterjugs = create_waterjugs_problem(0, 0, 2, 0)

    print("=========Test 1. Astar with h_sum heuristic========")
    waterjugs.set_heuristic(waterjugs_h_sum_function)
    astar_search(waterjugs, FullCheck(), 1)
    print("===================================================")
    print("")
    print("=========Test 2. Astar with h_max heuristic========")
    waterjugs.set_heuristic(waterjugs_h_max_function)
    astar_search(waterjugs, FullCheck(), 1)
    print("===================================================")
    print("")

    print("=========Test 3a. Breadth first (full cycle checking)==")
    breadthfirst_search(waterjugs, FullCheck(), 1)
    print("===================================================")
    print("")

    print("=========Test 3a. Breadth first with only path checking=====")
    breadthfirst_search(waterjugs, PathCheck(), 1)
    print("===================================================")
    print("")

    print("=========Test 3a. Breadth first with no cycle checking=====")
    breadthfirst_search(waterjugs, NullCheck(), 1)
    print("===================================================")
    print("")

    waterjugs = create_waterjugs_problem(0, 0, 2, 1)
    print("=========Test 4. Breadth first on unreachable goal with only path checking==")
    breadthfirst_search(waterjugs, PathCheck(), 1)
    print("========================================================")
    print("")

    print("=========Test 5. Breadth first on unreachable goal with full checking==")
    breadthfirst_search(waterjugs, FullCheck(), 1)
    print("========================================================")
    print("")

    print("=========Test 6. Depth first on unreachable goal with path checking==")
    depthfirst_search(waterjugs, PathCheck(), 1)
    print("========================================================")
    print("")
