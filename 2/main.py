import numpy as np
import os
import csv
import networkx as nx


def import_from_file(file):
    records = []
    G = nx.Graph()
    with open(file, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            records.append(row)
    G.add_nodes_from(list(map(lambda x: int(x[0]), records)))
    for i, record in enumerate(records):
        print(record, i)
        G.add_edge(int(record[0]), int(record[1]),  R=abs(int(record[2])), I=0, no=i)
        # G.add_edge(int(record[1]), int(record[0]),  R=abs(int(record[2])), I=0, no=i)

    return G


def KirI(G):
    eqs = []
    edges_count = len(G.edges)
    for n in G.nodes:
        Is = [0 for i in range(edges_count)]
        for e in G.edges(n):
            data = G.get_edge_data(*e)
            print(e, data['no'])
            Is[data['no']] = 1 if e[0] > e[1] else -1
        print('\n\n')
        eqs.append(Is)
    return eqs


def KirII(G):
    eq = []
    edges_count = len(G.edges)
    for cycle in nx.cycle_basis(G):
        Is = [0 for i in range(edges_count)]
        for i in range(len(cycle)):
            n1 = cycle[i]
            n2 = cycle[(i+1) % len(cycle)]
            data = G.get_edge_data(n1,n2)
            Is[data['no']] = data['R'] if n1 > n2 else -data['R']
        eq.append(Is)
    return eq


def create_equations(G):
    eqs = KirI(G)
    eqs += KirII(G)
    print(eqs)


G = import_from_file("small.csv")
create_equations(G)
#print(G.edges)