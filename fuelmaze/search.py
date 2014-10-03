import os

from problem import *
from open import *
from cyclecheck import *

# Search statistics
total_search_time = 0

def _print_goal(strategy, nodes_generated, nodes_expanded, cycle_check_pruned, total_search_time, goal_node):
    print("============================")
    print("Search Successful! (strategy '{}') Solution cost = {}, Goal state:".format(strategy, goal_node.gval))
    print("    " + str(goal_node))
    print("----------------------------")
    print("Solution Path:")
    for n in goal_node.path():
        print("    " + str(n))
    print("----------------------------")
    print("Search time = {}, nodes generated = {}, nodes expanded = {}, nodes cycle check pruned = {}".format(total_search_time, nodes_generated, nodes_expanded, cycle_check_pruned))

def _print_failure(strategy, nodes_generated, nodes_expanded, cycle_check_pruned, total_search_time):
    print("============================")
    print("Search Failed! (strategy '{}') No solution found".format(strategy))
    print("----------------------------")
    print("Search time = {}, nodes generated = {}, nodes expanded = {}, nodes cycle check pruned = {}".format(total_search_time, nodes_generated, nodes_expanded, cycle_check_pruned))

def _standard_search(problem, open_list, cycle_check, trace):
    # Reset passed-in parameters
    open_list.clear()
    cycle_check.clear()
    sNode.reset_nodes_expanded()

    # initialize search statistics
    total_search_time = os.times()[0]

    # Insert the initial state into the open list
    init_node = problem.get_initial_node()
    open_list.insert(init_node)

    # CYCLE-CHECK INITIAL NODE TO MAKE SURE IT IS ADDED TO THE DICTIONARY IF FULL-CHECKING
    cycle_check.prune(problem, init_node)

    #BEGIN TRACING
    if trace > 1:
        print("   TRACE: Initial OPEN: ", end=' ')
        open_list.print_open()
        print("   TRACE: Initial CC:", end=' ')
        cycle_check.print_debug()
    #END TRACING

    while not open_list.empty():
        node = open_list.extract()

        #BEGIN TRACING
        if trace > 1:
            print("   TRACE: Next State to expand: ", end=' ')
            print(node)
        #END TRACING

        # If node at front of OPEN is a goal...search is completed.
        if problem.goal_check(node.state):
            total_search_time = os.times()[0] - total_search_time
            if trace:
                _print_goal(open_list.print_type() + " with " + cycle_check.print_type(), sNode.nodes_generated, open_list.nodes_expanded, cycle_check.pruned_nodes, total_search_time, node)
            return node 

        # All states reached by a search node on open_list have already been hashed into the
        # full cycle checking dictionary. However, before expanding a node we might have 
        # already expanded an equivalent state with lower g-value. So only expand the node 
        # if the hashed g-value is no greater than the node's current g-value.
        if cycle_check.lazy_check(problem, node):
            #BEGIN TRACING
            if trace > 1:
                print("    TRACE: Pruned by already expanded state with lower g-value.")
            #END TRACING
            continue

        successors = node.expand(problem)
        if not successors:
            continue

        #BEGIN TRACING
        if trace > 1:
            print("    TRACE: Expanding Node. Successors = {")
            for ss in successors:
                print("        " + str(ss))
            print("    }")
        #END TRACING

        # Filter out prunable states
        successors = [succ for succ in successors if not cycle_check.prune(problem, succ)]

        #BEGIN TRACING
        if trace > 1:
            print("    TRACE: Successors after pruning = {")
            for ss in successors:
                print("        " + str(ss))
            print("    }")
        #END TRACING

        # Add all successors to the open list
        open_list.extend(successors)
    #end of while--OPEN is empty and no solution
    total_search_time = os.times()[0] - total_search_time
    if trace:
        _print_failure(open_list.print_type() + " with " + cycle_check.print_type(), sNode.nodes_generated, open_list.nodes_expanded, cycle_check.pruned_nodes, total_search_time)
    return None

def breadthfirst_search(problem, cycle_check=FullCheck(), trace=1):
    return _standard_search(problem, OpenBFS(), cycle_check, trace)

def depthfirst_search(problem, cycle_check=PathCheck(), trace=1):
    return _standard_search(problem, OpenDFS(), cycle_check, trace)

def bestfirst_search(problem, cycle_check=FullCheck(), trace=1):
    return _standard_search(problem, OpenBF(), cycle_check, trace)

def astar_search(problem, cycle_check=FullCheck(), trace=1):
    return _standard_search(problem, OpenAStar(), cycle_check, trace)

def idastar_search(problem, cycle_check=PathCheck(), trace=1):
    # Set initial F-bound as the heuristic estimate of the initial state
    bound = problem.heuristic(problem.initial)

    # Accumulated search statistics over all passes
    acc_nodes_generated = 0
    acc_nodes_expanded = 0
    acc_pruned_nodes = 0
    acc_total_search_time = 0

    while 1:
        # BEGIN TRACING
        if trace > 1:
            print("TRACE: Bound = {}".format(bound))
        # END TRACING

        # Run the search with the specified bound
        open_list = OpenIDAStar(bound)
        node = _standard_search(problem, open_list, cycle_check, 0)

        # Update accumulated statistics
        acc_nodes_generated += sNode.nodes_generated
        acc_nodes_expanded += open_list.nodes_expanded
        acc_pruned_nodes += cycle_check.pruned_nodes
        acc_total_search_time += total_search_time

        # Goal found
        if node:
            if trace:
                _print_goal(open_list.print_type() + " with " + cycle_check.print_type(), acc_nodes_generated, acc_nodes_expanded, acc_pruned_nodes, acc_total_search_time, node)
            return node
        # No goal found and no nodes with greater fval than the bound
        if open_list.min == -1:
            if trace:
                _print_failure(open_list.print_type() + " with " + cycle_check.print_type(), acc_nodes_generated, acc_nodes_expanded, acc_pruned_nodes, acc_total_search_time)
            return None
        # Set the new bound as the minimum fval that was larger than previous bound
        bound = open_list.min
