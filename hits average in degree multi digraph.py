
import networkx as nx
from networkx.exception import NetworkXError
import matplotlib.pyplot as plt
import scipy as sp
import numpy as np
G = nx.DiGraph()
[G.add_node(k) for k in [0,1,2,3,4,5,6,7,8,9]]
G.add_edges_from([(0,5),(1,5),(2,4),(3,4),(0,3),(4,6),(5,6),(5,4),(5,3),(6,7),(4,8),(3,9),(8,9),(6,9)])
__all__ = ['hits','hits_numpy','hits_scipy','authority_matrix','hub_matrix']
def hits(G,max_iter=100,tol=1.0e-8,nstart=None,normalized=True):
    if type(G) == nx.MultiGraph or type(G) == nx.MultiDiGraph:
        raise Exception("hits() not defined for graphs with multiedges.")
    if len(G) == 0:
        return {},{}
    # choose fixed starting vector if not given
    if nstart is None:
        h=dict.fromkeys(G,1.0/G.number_of_nodes())
    else:
        h=nstart
        s=1.0/sum(h.values())
        for k in h:
            h[k]*=s
    i=0
    while True:
        hlast=h
        h=dict.fromkeys(hlast.keys(),0)
        a=dict.fromkeys(hlast.keys(),0)
        for n in h:
            for nbr in G[n]:
                a[nbr]+=hlast[n]*G[n][nbr].get('weight',1)
        for n in h:
            for nbr in G[n]:
                h[n]+=a[nbr]*G[n][nbr].get('weight',1)
        s=1.0/max(h.values())
        for n in h: h[n]*=s
        s=1.0/max(a.values())
        for n in a: a[n]*=s
        err=sum([abs(h[n]-hlast[n]) for n in h])
        if err < tol:
            break
        if i>max_iter:
            raise NetworkXError(\
            "HITS: power iteration failed to converge in %d iterations."%(i+1))
        i+=1
    if normalized:
        s = 1.0/sum(a.values())
        for n in a:
            a[n] *= s
        s = 1.0/sum(h.values())
        for n in h:
            h[n] *= s
    print("\nHub Score:\n")
    print(h)
    print("\nAuthority Score:\n")
    print(a)

def authority_matrix(G,nodelist=None):
    M=nx.to_numpy_matrix(G,nodelist=nodelist)
    return M.T*M

def hub_matrix(G,nodelist=None):
    M=nx.to_numpy_matrix(G,nodelist=nodelist)
    return M*M.T


print(nx.info(G))
print("\n\n\nHub Matrix:\n")
print(hub_matrix(G))
print("\nAuthority Matrix:\n")
print(authority_matrix(G))
hits(G)
nx.draw(G)
plt.show()

