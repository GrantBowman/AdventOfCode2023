import re
# https://regex101.com/r/nH4nD3/3
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
import scipy as sp

# pygraph
#   python-graph-core, if needed for ^
# networkx
# matplotlib



sent = [0, 0]
debugPrint = True

class Node():
    def __init__(self, id=""):
        self.id = id
        self.edges = []
        self.visited = 0
    
    def __repr__(self):
        return f"Node {self.id}"
    def __str__(self):
        return f"Node {self.id}: {self.edges}"


G = nx.Graph()

with open("input25.txt") as input:
    print("hello world")
    
    # this holds Node: list(str dests)
    graphSetup = {}
    # this holds str: Node obj
    graphNodes = {}
    # this holds Nodes
    graph = []
    # need 2 passes: 1 to get a list of nodes, and a 2nd to connect them
    # first pass
    for line in input:
        ids = line.strip().split(" ")
        id = ids[0][:-1]
        destinations = ids[1:]
        # print(f"id={id}, destinations={destinations}")

        # create/get node id
        G.add_node(id)
        # add destinations to source
        for dest in destinations:
            G.add_edge(id, dest, capacity=1)

# if debugPrint: 
#     nx.draw(G, with_labels=True)
#     plt.show()
            

# just grabbing 2 random nodes: zql, qqb
# from visualization: dzr, tzg
cut_val, partition = nx.minimum_cut(G, "dzr", "tzg")
print(f"{cut_val}")
result = len(partition[0]) * len(partition[1])
print(result)

print("goodbye world")