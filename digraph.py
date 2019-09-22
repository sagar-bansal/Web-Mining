import networkx as nx
import matplotlib.pyplot as plt

g=nx.DiGraph()
g.add_edges_from([(1,2),(1,3),(3,1),(3,2),(2,3)])
nx.draw(g)
plt.show()
