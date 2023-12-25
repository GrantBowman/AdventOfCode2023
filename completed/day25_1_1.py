import re
# https://regex101.com/r/nH4nD3/3
from collections import deque


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

with open("input25_demo.txt") as input:
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
        n = None
        if id not in graphNodes.keys():
            n = Node(id=id)
            graph.append(n)
            graphNodes[id] = n
        else:
            n = graphNodes[id]
        # add destinations to source
        if n in graphSetup:
            for a in destinations:
                graphSetup[n].append(a)
        else:
            graphSetup[n] = destinations

        # destinations might not exist yet
        for destId in destinations:
            n = None
            if destId not in graphNodes.keys():
                n = Node(id=destId)
                graph.append(n)
                graphNodes[destId] = n
            else:
                n = graphNodes[destId]
            # destinations point back to source
            if n in graphSetup:
                graphSetup[n].append(id)
            else:
                graphSetup[n] = [id]

# second pass
# connect the nodes
for k, dests in graphSetup.items():
    # print(f"setup k={k}, v={dests}")
    for destId in dests:
        if destId in graphNodes:
            destNode = graphNodes[destId]
            if graphNodes[destId] not in k.edges:
                k.edges.append(destNode)
            if k not in graphNodes[destId].edges:
                destNode.edges.append(k)

if debugPrint: 
    for n in graph:
        print(n)
    print()


print("goodbye world")