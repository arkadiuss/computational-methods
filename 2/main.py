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
    for record in records:
        G.add_edge(int(record[0]), int(record[1]), R=abs(int(record[2])))

    return G


G = import_from_file("soc-sign-bitcoinalpha.csv")
print(G.edges)