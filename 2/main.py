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

    return G


def KirI(G):
    eqs = []
    edges_count = len(G.edges)
    for n in G.nodes:
        Is = [0 for i in range(edges_count)]
        for e in G.edges(n):
            print(e)
            data = G.get_edge_data(*e)
            Is[data['no']] = 1
        print('\n\n')
        eqs.append(Is)
    return eqs


#def KirII(G):


def create_equations(G):
    eqs = KirI(G)
    print(eqs)


G = import_from_file("small.csv")
create_equations(G)
#print(G.edges)