#!/usr/bin/env python
import pygraphviz
import networkx
import sys

if len(sys.argv) != 4 or (sys.argv[1] != "colo" and sys.argv[1] != "call"):
    print("Usage: " + sys.argv[0] + " colo/call input.dot output.am")
else:
    g = networkx.Graph(pygraphviz.AGraph(sys.argv[2]))
    f = open(sys.argv[3], "w+")
    for s, d, w in g.edges(data=True):
        label = ""
        if sys.argv[1] == "call":
            label = w["label"]
        elif sys.argv[1] == "colo":
            label = g.number_of_edges(s, d) # Should always be 1
        f.write(str(s) + ", " + str(d) + ", " + str(label) + " \n")
    f.close()