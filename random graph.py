# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 00:49:57 2018

@author: sagar
"""
#import igraph
#import numpy as np
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
G=nx.Graph()
for i in {1,2,3,4,5,6,7,8,9}:
    G.add_node(i)
nx.draw(G,with_labels=True)
n=np.random.randint(1,10+1)
#n is the number of vertices in the graph. 
adjacency = np.random.randint(0,,(n,n))

for i in {1,2,3,4,5,6,7,8,9}:
    for j in {1,2,3,4,5,6,7,8,9}:
        if(adjacency[i,j]==1):
            G.add_edge(i,j)
plt.show()

#G_best = igraph.Graph.Erdos_Renyi(n=n, p=p, directed=True, loops=False)