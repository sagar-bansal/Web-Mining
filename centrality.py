import matplotlib.pyplot as plt
import networkx as nx

G=nx.read_edgelist('node.txt',create_using=nx.Graph(),nodetype=int)
nx.draw(G,with_labels=True)
plt.show()
print(nx.closeness_centrality(G))
print(nx.degree_centrality(G))
