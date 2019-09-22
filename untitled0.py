# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 01:16:54 2018

@author: sagar
"""

import numpy as np
n=np.random.randint(1,10+1)
#n is the number of vertices in the graph. 
adjacency = np.random.randint(0,4,(n,n))
print(adjacency[1,3])