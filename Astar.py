# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import sys
import Graph
from collections import namedtuple
import Heuristic

def Astar(start, goal, graph):
	closedset = set()  #set of visited nodes    
	openset = {start}  #set of nodes to be evaluated  
	came_from = {}  #keeps track of path
	g_score = {}  #the cost from the start to current
	f_score = {}  #the cost of g_score + the heuristic cost of current to goal
	g_score[start] = 0    
	f_score[start] = g_score[start] + Heuristic.cost_of_path(start,  goal)
	while len(openset) > 0:
		lowest_cost = sys.maxint
		current = None
		for i in openset:  #find cheapest node in openset
			if f_score[i] < lowest_cost:
				#print i, f_score[i]
				lowest_cost = f_score[i]
				current = i
		if current == goal:
            #print "current is equal to goal"
			return reconstruct_path(came_from, goal)         
		#print "this is current", current
		openset.remove(current)
		closedset.add(current)
		if current not in came_from:
			came_from[current] = [current]
		else:
			came_from[current].append(current)
		for neighbor in graph.neighbor(current):
			#print "this is the neighbor", neighbor
			tentative_g_score = g_score_comp(current, came_from) + Heuristic.cost_of_path(current,neighbor)
			# if we have processed this node already but current path is cheaper, remove so we add new path
			if neighbor in g_score and tentative_g_score < g_score[neighbor]:
				if neighbor in closedset:
					closedset.remove(neighbor)
				if neighbor in openset:
					openset.remove(neighbor)
			if neighbor not in openset and neighbor not in closedset: 
				came_from[neighbor] = came_from[current][:]
				g_score[neighbor] = tentative_g_score
				f_score[neighbor] = g_score_comp(neighbor,came_from) + Heuristic.cost_of_path(neighbor,goal)
				if neighbor not in openset:
					openset.add(neighbor)

def reconstruct_path(came_from, goal):
	#print "returning shortest path", came_from[goal]
    if goal in came_from[goal]:
        came_from[goal].append(goal)
        #print "returning shortest path", came_from[goal]
    else:
        return came_from[goal]
        #print "returning shortest path", came_from[goal]

def g_score_comp(node, came_from):
	sumcost = 0
	for n in came_from[node]:
		#print n
		sumcost += n.cost
	return sumcost

