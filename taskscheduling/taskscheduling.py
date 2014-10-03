'''TaskScheduling Domain
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

class SchedulingState:


    #Implement this, you will have to alter the parameters
    def __init__(self):
        '''Initializes the state'''
        
    #To be implemented - for information purposes only
    def __repr__(self):
        '''Returns a string representation of the state'''
        return ret


class TaskScheduling(Problem):


    #Implement this, but DO NOT change the function parameters
    def __init__(self, configurations, jobs, starting_configuration):
        '''Initializes a task scheduling problem where
        
        *configurations is a list of configuration tuples
        each tuple ('c1',5) contains a string representing the name of the configuration and the cost of setting that configuration
        
        *jobs is a list of the jobs to be performed.  Each job is a tuple ('j1', 'c3', 10, 5, [(13,5),(19,7),(25,10),...])
        -A string representing the unique job name
        -A string representing the configuration the system must be in to perform the job
        -An integer representing the earliest possible time the job can be completed
        -An integer representing the time it takes to complete the job
        -A list of tuples (time, cost) representing penalty costs if the job is completed after that time
         only the largest penalty applies
        
        *starting_configuration is a string from a tuple in configurations, representing the configuration the system starts in 


        '''
        
        #Update this line to coincide with your constructor for SchedulingState
        #Problem.__init__(self, SchedulingState(...), SchedulingState(...))

        
    #Implement this!
    def successors(self, state):
        '''Return a list of (action, cost, successor) tuples where
           action is the string name of the action performed in state to reach successor
           cost is the cost of performing action in state
           successor is the result of performing action in state
           '''

        '''Valid action names:
        Set configuration('configurationname')
        Perform Task('jobname')
        '''
        
        
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

      #Any state in which we have finished all jobs should be a goal state
      return False
        

# The given NULL heuristic (do not change)
def h_uniform(problem, state):
    # Causes algorithm to do uniform cost search
    return 0

## Implement your own heuristic
def h_custom(problem, state):
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
    ## more to be added
    schedulingproblems = [
       
        TaskScheduling(
            [('c1', 10), ('c2', 15) , ('c3', 17) ,('c4', 14) ],
            [
                ('j1','c1',3,3, [(8,10)]),
                ('j2','c1',12,3,[(15,15)]),
                ('j3','c2',5,3, [(12,15)]),
                ('j4','c2',15,3,[(15,15)]),
                ('j5','c3',6,3, [(10,5)]),
                ('j6','c4',6,3, [(10,10)])
                ],
            'c1'
        )
                
                          
    ]
    
    heuristics = [
              ('Uniform heuristic', h_uniform),         
              ('Custom heuristic', h_custom) ]

    # Set this to >=1 to get increasingly informative search statistics
    trace = 1

    
    for m in range(len(schedulingproblems)):        
        
        currentproblem = schedulingproblems[m]
        
        for (hname, h) in heuristics:

            currentproblem.set_heuristic(h)

            print("====================================================")
            print("TaskScheduling {}, {}, A* with cycle checking".format(m+1, hname))
            node = astar_search(currentproblem, FullCheck(), trace)
            
            print("====================================================")
            print("")

