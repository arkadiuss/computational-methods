import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import scipy


def simple_rank(A):
    rank = np.real(np.array(np.linalg.eig(A)[1])[0])
    return rank / np.linalg.norm(rank)


def page_rank(A):
    pass


G = nx.generators.gnm_random_graph(20, 30, directed=True)


A = nx.adjacency_matrix(G).todense()
rank = np.squeeze(simple_rank(A))
print(rank)

lay = nx.spring_layout(G)
nx.draw_networkx_nodes(G,pos=lay, label=True, node_color=rank)
nx.draw_networkx_edges(G,pos=lay)
plt.show()
