import numpy as np
import os
import csv


class Edge:
    def __init__(self, u, v):
        self.u = u
        self.v = v


class Node:
    def __init__(self):
        self.edges = []


class Graph:
    def __init__(self, n=0):
        self.n = n
        self.G = [Node() for i in range(n)]

    def add_edge(self, a, b, w):
        e = Edge(b, w)
        self.G[a].edges.append(e)
        e = Edge(a, w)
        self.G[b].edges.append(e)

    def import_from_file(self, file):
        with open(file, "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self.n += 1



g = Graph()
g.import_from_file("soc-sign-bitcoinalpha.csv")


