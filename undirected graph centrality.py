# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 21:49:44 2018

@author: sagar
"""

import networkx as nx

import matplotlib.pyplot as plt


G=nx.read_edgelist('node.txt',create_using=nx.Graph(),nodetype=int)


print(nx.info(G))


nx.draw(G,with_labels=True)


print("\nDegree Centrality: ")

print(nx.degree_centrality(G))

print("\n The node with max degree centrality is")

print(max(nx.degree_centrality(G)));

print("\nBetweenness Centrality: ")

print(nx.betweenness_centrality(G))

print("\n The node with max betweenness centrality is")


print(max(nx.betweenness_centrality(G)));

print("\nCloseness Centrality: ")

print(nx.closeness_centrality(G))

print("\n The node with max closeness centrality is")

print(max(nx.closeness_centrality(G)))

plt.show()
 

