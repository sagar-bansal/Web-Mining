# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 00:44:30 2018

@author: sagar
"""

import igraph
import numpy as np

def generate_fixed_gcc(n, p, target_gcc, tol=1E-3):
    """
    Creates an Erdos-Renyi random graph of size n with a specified global
    connection probability p, which is then iteratively rewired in order to
    achieve a user- specified global clustering coefficient.
    """

    # initialize random graph
    G_best = igraph.Graph.Erdos_Renyi(n=n, p=p, directed=True, loops=False)

    loss_best = 1.
    n_edges = G_best.ecount()

    # start with a high rewiring rate
    rewiring_rate = n_edges
    n_iter = 0

    while loss_best > tol:

        # operate on a copy of the current best graph
        G = G_best.copy()

        # adjust the number of connections to rewire according to the current
        # best loss
        n_rewire = min(max(int(rewiring_rate * loss_best), 1), n_edges)
        G.rewire(n=n_rewire)

        # compute the global clustering coefficient
        gcc = G.transitivity_undirected()
        loss = abs(gcc - target_gcc)

        # did we improve?
        if loss < loss_best:

            # keep the new graph
            G_best = G
            loss_best = loss
            gcc_best = gcc

            # increase the rewiring rate
            rewiring_rate *= 1.1

        else:

            # reduce the rewiring rate
            rewiring_rate *= 0.9

        n_iter += 1

    # get adjacency matrix as a boolean numpy array
    M = np.array(G_best.get_adjacency().data, dtype=np.bool)

    return M, n_iter, gcc_best