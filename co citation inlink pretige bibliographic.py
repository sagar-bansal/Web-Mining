import networkx as nx
import matplotlib.pyplot as plt

g = nx.DiGraph()
g.add_edges_from([(1, 2), (1, 3), (3, 1), (3, 2), (2, 4), (3, 4), (4, 3)]) 
print (nx.info(g))
print ("Degree Prestige:")
degree_prestige = dict((v, len(g.in_edges(v))/(g.number_of_nodes() - 1)) for v in list(g.nodes))
print (degree_prestige)
print ("*******")
length = nx.all_pairs_shortest_path_length(g)
d = dict(length)
final_dict = {}
for i in range(1, g.number_of_nodes()+1):
    k = 0
    counter=0
    for j in range(1, g.number_of_nodes()+1):
        try:
            k = k + d[j][i]
            counter+=1
        except:
            break
    final_dict[i] = k/(counter-1)
print ('Proximity Prestige')
print (final_dict)
print ('*************')

input_user = 2
l = []
h = {}
for i in range(0, g.number_of_nodes()):
    a = 1/g.number_of_nodes()
    h[i+1] = a
l.append(h)
    
x = 1
while (x<=input_user):
    h1 = {}
    for i in range(1, g.number_of_nodes()+1):
        iter_list1 = list(g.in_edges(i))
        sum1 = 0
        for j in range(0, len(iter_list1)):
            first_one = iter_list1[j][0]
            sum1 = l[x-1][first_one]/g.out_degree(first_one) + sum1
        h1[i] = sum1
    l.append(h1)
    x = x+1
matrix = nx.to_numpy_matrix(g)
list1 = matrix.tolist()
final_list = []
for i in range(0, len(list1)):
    trial = []
    for j in range(0, len(list1)):
        sum3 = 0
        for k in range(0, len(list1)):
            sum3 = list1[k][j]*list1[k][i] + sum3
        trial.append(sum3)
    final_list.append(trial)
print ("Co-Citation:")
print (final_list)

print ('********')
final_coupling = []
for i in range(0, len(list1)):
    trial_2 = []
    for j in range(0, len(list1)):
        sum4 = 0
        for k in range(0, len(list1)):
            sum4 = sum4 + list1[i][k]*list1[j][k]
        trial_2.append(sum4)
    final_coupling.append(trial_2)
print ("Bibliographic Coupling:")
print (final_coupling)
print ("******")
print ("Page Rank:")
print (nx.pagerank(g))
nx.draw(g)
plt.show()
