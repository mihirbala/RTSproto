# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from collections import namedtuple
from Graph import Graph

node_pair_cost_map = {}

def cost_of_path(node, goal):
    if node.cost == 10000:
        return 10000
    else:
        #print 'not expensive node pair', node.x, node.y
        dx = abs(node.x - goal.x)
        dy = abs(node.y - goal.y)
        return 1 * (dx + dy)


def heuristic_estimate(graph):
    global node_pair_cost_map
    for node1 in graph.get_nodes():
        for node2 in graph.get_nodes():
            node_pair_cost_map[(node1, node2)] = cost_of_path(node1, node2)

