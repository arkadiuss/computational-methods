import numpy as np
import os
import csv
import networkx as nx
import matplotlib.pyplot as plt


def import_from_file(file):
    records = []
    G = nx.Graph()
    with open(file, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            records.append(row)
    G.add_nodes_from(list(map(lambda x: int(x[0]), records)))
    for i, record in enumerate(records):
        # print(record, i)
        G.add_edge(int(record[0]), int(record[1]), R=abs(int(record[2])), no=i + 1, sem=0)
    return G


def KirI(G):
    eqs = []
    b = []
    edges_count = len(G.edges)
    for n in G.nodes:
        Is = [0 for i in range(edges_count)]
        b.append(0)
        for e in G.edges(n):
            data = G.get_edge_data(*e)
            print(e, data['no'])
            Is[data['no']] = 1 if e[0] > e[1] else -1
        print('\n\n')
        eqs.append(Is)
    return eqs, b


def KirII(G):
    eq = []
    b = []
    edges_count = len(G.edges)
    for cycle in nx.cycle_basis(G):
        # print(cycle)
        Is = [0 for i in range(edges_count)]
        b.append(0)
        for i in range(len(cycle)):
            n1 = cycle[i]
            n2 = cycle[(i + 1) % len(cycle)]
            data = G.get_edge_data(n1, n2)
            Is[data['no']] = data['R'] if n1 > n2 else -data['R']
            b[-1] += data['sem'] if n1 > n2 else -data['sem']
        eq.append(Is)
    return eq, b


def create_equations(G):
    eqs, b = KirI(G)
    eqs2, b2 = KirII(G)
    eqs = eqs + eqs2
    b = b + b2
    return eqs, b


G = import_from_file("small.csv")
G.add_edge(1, 4, R=0, sem=3, no=0)
I, E = create_equations(G)
res = np.linalg.lstsq(I, E, rcond=None)[0]

print(res)

for i, e in enumerate(G.edges):
    G[e[0]][e[1]]['I'] = res[G[e[0]][e[1]]["no"]]
    print("edge: ", e, "no: ", G[e[0]][e[1]]["no"], "I: ", G[e[0]][e[1]]['I'])

elarge = [(u, v) for (u, v, d) in G.edges(data=True) if abs(d['I']) > 0.5]
esmall = [(u, v) for (u, v, d) in G.edges(data=True) if abs(d['I']) <= 0.5]

pos = nx.spring_layout(G)  # positions for all nodes

# nodes
nx.draw_networkx_nodes(G, pos, node_size=700)

# edges
nx.draw_networkx_edges(G, pos, edgelist=elarge,
                       width=6)
nx.draw_networkx_edges(G, pos, edgelist=esmall,
                       width=6, alpha=0.5, edge_color='b', style='dashed')

# labels
nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')

plt.axis('off')
plt.show()
