from fuelmaze import *


'''----------------------------------------------------------------------
   Definitions of three sample instances that you will run your code. 
   Do not change these! 
   You are strongly encouraged to also test your code with other fuelmazes
     of various sizes and start/goal positions (simply add
    more fuelmazes to the list).
-------------------------------------------------------------------------'''

#Helper function for a procedurally generated maze
#The maze is 7 tiles high and 1+ 12*the entered number tiles long
#The maze requires some detours due to fuel and obstacle issues, but is solvable
def mazegen(length):


    obstacles = []
    fuelstations = [(0,0), (0,6)]

    for i in range(0,length):
        obstacles.append( (3 + 12 * i,6) )
        obstacles.append( (9 + 12 * i,0) )
        fuelstations.append( (6 + 12 * i,0))
        fuelstations.append( (12 + 12 * i,0))
        fuelstations.append( (6 + 12 * i,6))
        fuelstations.append( (12 + 12 * i,6))
 

    return Fuelmaze(length * 12 + 1,  7, 6,    
                fuelstations, 
                obstacles,                                        
                (0,0), 0, (12*length,0))

    


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
                 (0,0), 30, (7,1)),
        Fuelmaze(10, 10, 15,        #A simple case that is unsolvable due to lack of fuel
                 [],
                 [], 
                 (0,0), 15, (9,9)),
        Fuelmaze(10, 10, 50,        #A simple case that is unsolvable due to an unreachable goal
                 [],
                 [(6,7),(8,7),(7,6),(7,8)], 
                 (0,0), 50, (7,7)),
        Fuelmaze(10, 10, 4,         #A simple case that can only finish with zero fuel remaining
                 [],
                 [], 
                 (0,0), 4, (0,4)),
        Fuelmaze(10, 10, 1,         #With a capacity of 1, the robot must follow the fuel stations to the end
                 [(0,1),(0,2),(1,2),(2,2),(3,2),(3,3),(3,4),(3,5),(3,6),(4,6),(4,7)],
                 [], 
                 (0,0), 1, (5,7)),
        mazegen(1),
        mazegen(5),
        #larger mazegen numbers can stress poor heuristics and slow computers
        #mazegen(100)
        
        
    ]
    

    


    heuristics = [
        ('Uniform heuristic', fuelmaze_h_uniform), 
        ('Manhattan-Distance heuristic', fuelmaze_h_manhattan),
        ('Custom heuristic', fuelmaze_h_custom) 
    ]

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
