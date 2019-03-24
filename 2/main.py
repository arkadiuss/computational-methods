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
            #print(e, data['no'])
            Is[data['no']] = 1 if e[0] > e[1] else -1
        #print('\n\n')
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

#print(res)


for i, e in enumerate(G.edges):
    G[e[0]][e[1]]['I'] = res[G[e[0]][e[1]]["no"]]
    # print("edge: ", e, "no: ", G[e[0]][e[1]]["no"], "I: ", G[e[0]][e[1]]['I'])

digraph = nx.DiGraph()
digraph.add_nodes_from(G)

max_I = -1

for i, e in enumerate(G.edges):
    #print(e, G[e[0]][e[1]]['I'])
    if G[e[0]][e[1]]['I'] > 0:
        digraph.add_edge(max(e[0],e[1]), min(e[0],e[1]), I=G[e[0]][e[1]]['I'])
    else:
        digraph.add_edge(min(e[0],e[1]), max(e[0],e[1]), I=abs(G[e[0]][e[1]]['I']))
    if abs(G[e[0]][e[1]]['I']) > max_I:
        max_I = abs(G[e[0]][e[1]]['I'])





pos = nx.spring_layout(digraph)  # positions for all nodes

# nodes
nx.draw_networkx_nodes(digraph, pos, node_size=700)


nx.draw_networkx_edges(digraph, pos,width=3,arrowstyle='->', edge_color='b')


# labels
nx.draw_networkx_labels(digraph, pos, font_size=20, font_family='sans-serif')

plt.axis('off')
plt.show()



