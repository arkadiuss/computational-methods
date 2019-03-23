import numpy as np
import os

class Edge:
    def __init__(self, u, v):
        self.u = u
        self.v = v


class Node:
    def __init__(self):
        self.edges = []


class Graph:
    def __init__(self, n):
        self.n = n
        self.G = [Node() for i in range(n)]

    def add_edge(self, a, b, w):
        e = Edge(b, w)
        self.G[a].edges.append(e)
        e = Edge(a, w)
        self.G[b].edges.append(e)


#    def import_from_file(file):

