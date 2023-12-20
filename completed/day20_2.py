import re
# https://regex101.com/r/nH4nD3/3
from collections import deque
import time

sent = [0, 0]
debugPrint = False

class Node():
    def __init__(self, label="", modType="=", state=0):
        self.label = label
        self.modType = modType
        self.state = state
        self.in_nodes = []
        self.out_nodes = []
    def __str__(self):
        return f"""\
{self.label:>5}: {self.state} {self.modType} -- in: [{', '.join(n.q_str() for n in self.in_nodes)}]
              out: [{', '.join(n.q_str() if n else "None" for n in self.out_nodes)}]"""
    def q_str(self):
        return f"({self.label} {self.modType} {self.state})"
    def __eq__(self, other):
        if isinstance(other, Node):
            return self.label == other.label
        else:
            return NotImplemented
    def __hash__(self):
        return hash((self.label, self.modType))

    def add_in_node(self, n):
        self.in_nodes.append(n)
        if n and self not in n.out_nodes:
            n.add_out_node(self)
    def add_out_node(self, n):
        self.out_nodes.append(n)
        if n and self not in n.in_nodes:
            n.add_in_node(self)
    def get_in_nodes(self):
        return self.in_nodes
    def get_out_nodes(self):
        return self.out_nodes
    def get_state(self):
        return self.state
    
    def eval(self, pulse):
        # if debugPrint: print(f"pulse received: {pulse} -> ({self.q_str()})")
        propogations = []
        # reserved for broadcaster, send 0s to all outnodes
        if self.modType == "=":
            for n in self.out_nodes:
                if debugPrint: print(f"sending pulse: {self.q_str()} -> {self.state} -> {n.q_str() if n else 'None'}")
                sent[0] += 1
                propogations.append((n, 0))
                # n.eval(0)
        if self.modType == "%":
            if pulse == 0:
                self.state = 0 if self.state else 1
                for n in self.out_nodes:
                    if debugPrint: print(f"sending pulse: {self.q_str()} -> {self.state} -> {n.q_str() if n else 'None'}")
                    sent[self.state] += 1
                    propogations.append((n, self.state))
                    # n.eval(self.state)
        if self.modType == "&":
            result = 0
            for n in self.in_nodes:
                if debugPrint: print(f"conjunction: {self.q_str()} looking at {n.q_str() if n else 'None'}")
                if n.get_state() == 0:
                    if debugPrint: print(f"conjunction: not all 1! sending 1")
                    result = 1
                    break
            self.state = result
            for n in self.out_nodes:
                sent[result] += 1
                if debugPrint: print(f"sending pulse: {self.q_str()} -> {result} -> {n.q_str() if n else 'None'}")
                propogations.append((n, result))
                # n.eval(result)
        return propogations


with open("input20.txt") as input:
    print("hello world")
    sum = 0
    startTime = time.time()

    i = 0
    
    graphSetup = {}
    graphNodes = {}
    graph = []
    # need 2 passes: 1 to get a list of nodes, and a 2nd to connect them
    for line in input:
        found = re.findall(r"([&%])?(\w+) -> ((?:\w+(?:, )?)*)", line.strip())
        if debugPrint: print(found)
        modType, label, destinations = found[0]
        modType = "=" if not modType else modType
        destinations = destinations.split(", ")
        n = Node(label=label, modType=modType)
        graph.append(n)
        graphNodes[label] = n
        graphSetup[n] = destinations
        pass
    # special "rx" node
    if "rx" not in graphNodes.keys():
        n = Node(label="rx", modType="=")
        graph.append(n)
        graphNodes["rx"] = n
        graphSetup[n] = []
    # connect the nodes
    for k, dests in graphSetup.items():
        for label in dests:
            if label in graphNodes:
                k.add_out_node(graphNodes[label])
            else:
                k.add_out_node(None)
        if debugPrint: print(k.q_str(), dests)
    if debugPrint: 
        for n in graph:
            print(n)
        print()

    broadcaster = graphNodes["broadcaster"]
    propogations = deque()

    # find the rx in nodes
    rxNodes = []
    rx = graphNodes["dt"]
    for n in graph:
        if rx in n.get_out_nodes():
            rxNodes.append(n)
            print(f"rx adjacent: {n.q_str()}")

    i = 0
    while True:
        i += 1
        done = False
        # low signal send from starting button
        sent[0] += 1
        if debugPrint: print(f"sending pulse: button -> 0 -> {broadcaster.q_str()}")
        propogations.append((broadcaster, 0))
        while propogations:
            isRxNode = False
            rxState = -1
            n, p = propogations.popleft()
            if n == None:
                continue
            if n == "rx":
                print(f"{i} button presses")
                done = True
                break
            # wrap rx adjacent state change detection v v v
            if n in rxNodes:
                isRxNode = True
                rxState = n.get_state()
            result = n.eval(p)
            if n in rxNodes:
                if rxState != n.get_state():
                    print(f"{n.q_str()} state flopped on iter {i}!")

            # wrap rx adjacent state change detection ^ ^ ^

            for r in result:
                propogations.append(r)
        if done:
            break
        if debugPrint: print(sent)
    print(sent)
    print(sent[0]*sent[1])
    endTime = time.time()
    runTime = endTime - startTime
    print(f"time taken: {runTime}")

    # graph = []
    # n1 = Node("n1", "%")
    # n2 = Node("n2", "%")
    # n3 = Node("n3", "&")
    # graph.append(n1)
    # graph.append(n2)
    # graph.append(n3)
    # # for n in graph:
    # #     print(n)
    # n1.add_out_node(n2)
    # n2.add_out_node(n3)
    # for n in graph:
    #     print(n)

    # n1.eval(0)
    # print(sent)

    # LCM after printing
    # pm = 287475, 291308, 295141, 298974 | 3833
    # ks = 289858, 293775, 297692, 301509 | 3917
    # dl = 290213, 293982, 297751, 301520 | 3769
    # vk = 290775, 294652, 298529, 302406 | 3877
    # ^ all in a conjunction for dt->rx, so need all = 1 to propogate out of dt and into rx
    # LCM = 
    # 3833 3917 3769 3877
    # v v v
    # 219,388,737,656,593
    # 219388737656593



print("goodbye world")