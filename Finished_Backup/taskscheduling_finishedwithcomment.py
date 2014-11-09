'''TaskScheduling Domain
Starter code for 384-A1, Last modified: September 30th, 2014

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%
%%  CSC384 Fall 2014, Assignment 1
%%
%%  NAME: Cai Lingfeng
%%
%%  STUDENT NUMBER: 1001931573
%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
'''

from problem import *
from math import *

class SchedulingState:


    #Implement this, you will have to alter the parameters
    def __init__(self, conf, time, job_completed ):
        '''Initializes the state'''
        
        self.conf = conf
        self.time = time
        self.job_completed = job_completed

    #To be implemented - for information purposes only
    def __repr__(self):
        '''Returns a string representation of the state'''
        ret = "(configuration, time, job_completed) = ({},{},{})".format(self.conf, self.time, self.job_completed)
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

        simplified_jobs = []
        i = 0
        while ( i < len(jobs)):
            simplified_jobs.append(jobs[i][0])
            i = i + 1
        
        #Update this line to coincide with your constructor for SchedulingState
        Problem.__init__(self, SchedulingState(starting_configuration, 0, []), SchedulingState(0, 0, simplified_jobs))

        self.configurations = configurations
        self.jobs = jobs
        self.starting_configuration = starting_configuration
        
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
        
        # Set configuration
        for conf in self.configurations:
            if conf != state.conf:
                States.append( ("Set Configuration(" + conf[0] + ")", conf[1], 
                    SchedulingState(conf , state.time + conf[1], state.job_completed) ) )

            
        # Perform task
        
        # job_remaining = list(set(self.jobs) - set(state.job_completed))
        for job in self.jobs:

            if job[0] not in state.job_completed:
                # if state.conf != job[1]:
                    # print (state.conf, job[1])
                if state.conf[0] == job[1] and state.time >= (job[2] - job[3]):
                    time_cost = 0
                    first_time = True

                    # Calculate the cost of time
                    for ddl in job[4]:
                        if ddl[0] < state.time + job[3]:
                            if first_time:
                                time_cost = ddl[1]
                                first_time = False
                            else:
                                time_cost = max(time_cost, ddl[1])
                    # print (type(state.job_completed))
                    # print (state.job_completed)
                    # print (job)  
                    new_job_list = list(state.job_completed)
                    new_job_list.append(job[0])
                    # print (new_job_list)

                    States.append( ( "Perform Task(" + job[0] + ")", time_cost, 
                        SchedulingState(state.conf , state.time + job[3], new_job_list) ) )
        # i = 0
        # while(i<len(States)):
        #      print (States[i][0],States[i][1],States[i][2])
        #      i = i + 1
        # print (States[0][0])
        # print (States[0][1])
        # print (States[0][2])
        # print ("State[0][0] is {}, State[0][1] is {}, State[0][2] is{}").format(States[0][0],States[0][1],States[0][2])
        return States


    #Implement this!
    def hashable_state(self, state):
        '''Return a tuple of the state's values that represents the state 
           such that equivalent states result in equivalent tuples.'''
        simplified_job_completed = list(state.job_completed)
        
        # simplified_job_completed = []
        # i = 0
        # while ( i < len(state.job_completed)):
        #     simplified_job_completed.append(state.job_completed[i][0])
        #     i = i + 1
        # print (simplified_job_completed)
        sorted_job_completed = sorted(simplified_job_completed, key=lambda job : job[0])
        sorted_tuple = tuple(sorted_job_completed)
        # print (sorted_tuple)
        # sorted_job_completed = sorted(a, key=lambda job : job[0])
        # return (state.conf, state.time, sorted_job_completed)
        # return (state.conf, state.time, "string", "strange")
        return (state.conf, 0, sorted_tuple)#state.job_completed)

    #Implement this!
    def goal_check(self, state):  

      #If we had a single goal state we could use the following test:
      #return self.hashable_state(self.goal) == self.hashable_state(state)

      #Any state in which we have finished all jobs should be a goal state
      return self.hashable_state(self.goal)[2] == self.hashable_state(state)[2]
        

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

