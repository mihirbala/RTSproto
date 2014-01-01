# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

class Graph:
    
    def __init__(self):
        self.nodes = set()
        self.edges = []
        self.node_edge_map = {}

    def print_graph(self):
        for edge in self.edges:
            print edge['source'], "->", edge['target']
            
    def add_node(self, node):
        self.nodes.add(node)

    def add_edge(self, edge):
        self.edges.append(edge)

    def get_nodes(self):
        return frozenset(self.nodes)

    def get_edges(self):
        return self.edges.iteritems()

    def add_edge(self, source, target):
        edge = {
            'source' : source,
            'target' : target,
            }
        self.edges.append(edge)
        if source in self.node_edge_map:
            self.node_edge_map[source].append(edge)
        else:
            self.node_edge_map[source] = [edge]

    def neighbor(self, source):
        neighbor_list = []
        for edge in self.node_edge_map[source]:
            neighbor_list.append(edge['target'])
        return neighbor_list

