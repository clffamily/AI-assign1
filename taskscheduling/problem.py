'''Abstract base classes defining problems and search nodes'''

#Zero Heuristic Function---for uninformed search
def _zero_hfn(problem, state):
    '''Null heuristic (zero)'''
    return 0

class Problem:

    '''Abstract base class defining the successor function and handling goal/initial states'''

    def __init__(self, initial, goal, heur_fn=_zero_hfn):
        '''Problem-derived classes must handle keeping the goal state and the number of states
        generated through it's successor function (see WaterJugs). Must keep the same names'''
        self.initial = initial # The initial state must be a fully specified state
        self.goal = goal # The goal state can either be a full or partial state
        self.heur_fn = heur_fn # The heuristic function for a state

    def set_heuristic(self, heur_fn):
        self.heur_fn = heur_fn

    def heuristic(self, state):
        return self.heur_fn(self, state)

    def get_initial_node(self):
        return sNode(self.initial, 0, self.heuristic(self.initial), None, "")

    def successors(self, state):
        '''Given a state, return all reachable successor states in a list.
           Must override.'''
        pass

    def goal_check(self, state):
        '''Checks whether the input state is a goal.
           Must override.'''
        pass

    def hashable_state(self, state):
        '''Returns the hashable version of a state. Can be used to check for equivalence between states.
           Must override.'''
        pass


class sNode:
    '''Node base class'''
    nodes_generated = 0

    def __init__(self, state, gval, hval, parent=None, action=""):
        '''Initialize node'''
        self.state = state
        self.gval  = gval
        self.hval  = hval
        self.parent = parent
        self.action = action
        self.index = sNode.nodes_generated
        if parent:
            self.depth = parent.depth + 1
        else:
            self.depth = 0

        sNode.nodes_generated += 1

    def __repr__(self):
        ret = "<Action=\"{}\",index={},g={},h={},f=g+h={}:S[{}],".format(self.action, self.index, self.gval, self.hval, self.gval+self.hval, self.state)
        if self.parent:
            ret += "(From Node{})>".format(self.parent.index)
        else:
            ret += "(Initial State)>"
        return ret

    def set_index(self, index):
        self.index = index

    def has_path_cycle(self, problem):
        '''Returns true if self has equal state to a prior node on its path'''
        s = self.parent
        hc = problem.hashable_state(self.state)
        while s:
            if problem.hashable_state(s.state) == hc:
                return True
            s = s.parent
        return False

    def path(self):
        '''Create a list of nodes from the root to this node.'''
        x = self
        ret = []
        while x:
            ret.append(x)
            x = x.parent
        ret.reverse()
        return ret

    def expand(self, problem):
        '''Returns a list of successor nodes reachable from this one.'''
        successors = problem.successors(self.state)
        successor_nodes = []
        for (act, cost, succ) in successors:
            successor_nodes.append(sNode(succ, self.gval + cost, problem.heuristic(succ), self, act))
        return successor_nodes

    @staticmethod
    def reset_nodes_expanded():
        sNode.nodes_generated = 0
