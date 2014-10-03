'''FuelMaze Domain
Starter code for 384-A1, Last modified: September 30th, 2014

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%
%%  CSC384 Fall 2014, Assignment 1
%%
%%  NAME: 
%%
%%  STUDENT NUMBER: 
%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
'''

from problem import *
from math import *

class FuelmazeState:

    def __init__(self, pos, fuel):
        '''Initializes the state where
             pos is a (X,Y) tuple representing the robot position,
             fuel is the remaining fuel supply of the robot
             '''
        self.pos = pos
        self.fuel = fuel

    def __repr__(self):
        '''Returns a string representation of the state (i.e. the robot position)'''
        ret = "(X, Y, fuel) = ({},{},{})".format(self.pos[0], self.pos[1],self.fuel)
        return ret

class Fuelmaze(Problem):

    def __init__(self, width, height, capacity, fuelstations, obstacles, start_pos, start_fuel, goal_pos):
        '''Initializes a fuelmaze where
             width is the size of the maze along the x-axis,
             height is the size of the maze along the y-axis (y-axis points downward),
             capacity is the amount of fuel the robot can carry
             fuelstations is a list of (X,Y) tuples representing where there are fuel stations in the maze,
             obstacles is a list of (X,Y) tuples representing where there are obstacles in the maze,
             start_pos is a (X,Y) tuple representing the start position,
             start_fuel is the amount of fuel the robot starts with,
             goal_pos is a (X,Y) tuple representing the goal position.
           Do not change.'''
        Problem.__init__(self, FuelmazeState(start_pos,start_fuel), FuelmazeState(goal_pos,0))

        self.width = width
        self.height = height
        self.capacity = capacity
        self.fuelstations = fuelstations
        self.obstacles = obstacles

    #Implement this!
    def successors(self, state):
        '''Return a list of (action, cost, successor) tuples where
           action is the string name of the action performed in state to reach successor
           cost is the cost of performing action in state
           successor is the result of performing action in state
           '''

        '''Valid action names:
           Right
           Left
           Up
           Down
           Refuel'''
        

        
        States = list()
        
        #Generate the states here
        
        return States


    #Implement this!
    def hashable_state(self, state):
        '''Return a tuple of the state's values that represents the state 
           such that equivalent states result in equivalent tuples.'''
        return 

    #Implement this!
    def goal_check(self, state):
        #If we had a single goal state we could use the following test:
        #return self.hashable_state(self.goal) == self.hashable_state(state)

        #We do not specify a target fuel in our goal states, alter this test so that
        #it only checks position, not fuel
        return False
        

# The given NULL heuristic (do not change)
def fuelmaze_h_uniform(problem, state):
    # Causes algorithm to do uniform cost search
    return 0

## Implement the Manhattan Distance
def fuelmaze_h_manhattan(problem, state):
    return 0

## Implement your own heuristic
def fuelmaze_h_custom(problem, state):
    return 0




'''----------------------------------------------------------------------
   Definitions of three sample instances that you will run your code. 
   Do not change these! 
   You are strongly encouraged to also test your code with other fuelmazes
     of various sizes and start/goal positions (simply add
    more fuelmazes to the list).
-------------------------------------------------------------------------'''
if __name__ == "__main__":

    from search import *

    ## TEST CASES
    ## A LIST OF FUELMAZES TO BE TESTED:
    ## fuelmaze1: 9x9 fuelmaze, start 1/1, goal 9/9
    ## fuelmaze2: 9x9 fuelmaze, start 1/1, goal 9/9 
    ## fuelmaze3: 9x9 fuelmaze, start 1/1, goal 8/2
    fuelmazes = [
        Fuelmaze(9, 9, 25,
                 [(8,6)],
                 [(3,0), (3,1), (2,2), (1,3), (1,6), (1,7), (0,8), (2,5), (3,4), (4,3), 
                  (5,2), (5,1), (6,1), (6,4), (6,5), (7,6), (5,5), (5,7), (8,7)], 
                 (0,0), 25, (8,8)),
        Fuelmaze(9, 9, 10,
                 [(0,8)],
                 [(0,1), (2,3), (4,4), (5,6), (0,6), (7,4), (8,7), (7,6), (4,8), (5,8)], 
                 (0,0),10, (8,8)),
        Fuelmaze(9, 9, 30,
                 [],
                 [(1,0), (2,1), (3,2), (3,4), (2,5), (1,6), (4,3), (5,2), (6,1), (5,5), 
                  (6,6), (7,7), (4,4)],
                 (0,0), 30, (7,1)) 
    ]
    
    heuristics = [
              ('Uniform heuristic', fuelmaze_h_uniform), 
              ('Manhattan-Distance heuristic', fuelmaze_h_manhattan),
              ('Custom heuristic', fuelmaze_h_custom) ]

    # Set this to >=1 to get increasingly informative search statistics
    trace = 1

    
    for m in range(len(fuelmazes)):        
        
        maze = fuelmazes[m]
        
        for (hname, h) in heuristics:

            maze.set_heuristic(h)

            print("====================================================")
            print("Fuelmaze {}, {}, A* with cycle checking".format(m+1, hname))
            node = astar_search(maze, FullCheck(), trace)
            
            print("====================================================")
            print("")

