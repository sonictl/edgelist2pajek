
import os
import networkx as nx


def ocp_space(i):   # assign some num of spaces before each line of vertices.
    total_len = len(str(num_vertices)) + 2
    i = int(i)
    i_len = len(str(i)) + 1
    return ' '*(total_len - i_len)


'''
 Code with Python > 3.5
 
 Convert Edgelist into .net file; covert class file into .clu file(optimal)
 each edge is separated by space, e.g. '100 101'
 > input file of edgelist: 
   ---
    v1  v2
    v3  v1
    v2  v3
   ---
 > input file of class:
   ---
    label  class
    v1     1
    v2     0
    v3     0
    ...
   ---
   
 BEFORE run, configure:
   - path of edgelist.txt
   - path of classes.txt (optional, classes_path = '' if there is no classes.txt file)
   - folder path for saving output files
   - specify directed or undirected graph: G = nx.Graph() or G = nx.DiGraph()
   - type number of your arcs, default: 1, (keep it as default if no specific need) 
   - type number of your edges, default: 2,(keep it as default if no specific need) 
'''

# path of edgelist:
edgelist_path = 'input/edgelist_test.txt'
# path of classes:
classes_path = 'input/classes_test.txt'   # classes_path = '' , if classes file is not exist.
# folder path for saving output files
output_folder = 'output'
# type of edges, 'directed' or 'undirected'
type_edges = 'directed'
# name of your network
name_network = 'Test_net'
# type No. of arcs, keep default.
typeNo_arcs = 1      # type number of each arc, specify the type of acrs
typeNo_edge = 2

# ======== Prepare of conversion =============
edgelist = []
nodeId_set = set()
with open(edgelist_path, 'r') as edgelistX_reader:  # input anchor for bind
    for line in edgelistX_reader.readlines():
        temp_array = line.strip().split()  #
        # edgelist.append(list(map(int, temp_array)))   # map to int
        edgelist.append(temp_array)   # keep the node_idx as string
        nodeId_set.add(temp_array[0])
        nodeId_set.add(temp_array[1])
edgelistX_reader.close()

edges = [tuple(e) for e in edgelist]
node_names = [n for n in nodeId_set]
node_names.sort()     # sort the 'label's, optional

if type_edges == 'directed':
    G = nx.DiGraph()  # Directed Graph
elif type_edges == 'undirected':
    G = nx.Graph()
else:
    assert False, 'Specify the right type of your graph.'

G.name = name_network
G.add_nodes_from(node_names)
G.add_edges_from(edges)
print(nx.info(G) + '\n---')    # graph is loaded.

# Create a mapping dictionary for vertices' names in Pajek,
paj_idx = [i+1 for i in range(nx.number_of_nodes(G))]  # the node_name in Graph above is treated as label in Pajek.
label_dic = dict(zip(paj_idx, node_names))       # pajek_idx(int) -> node_name/label(string)
label_dic_rev = dict(zip(node_names, paj_idx))   # node_name/label(string) -> pajek_idx(int)

# Prepare the output path for .net and .clu files
assert os.path.exists(output_folder), 'oops! The folder for storing the output does NOT exist!'
assert len(name_network) > 0, 'oops! The name of network is not specified!'
out_path_net = output_folder + '/' + name_network + '.net'    # path for saving the .net file
out_path_clu = output_folder + '/' + name_network + '.clu'    # path for saving the .clu file

# ==== Gen the .net file ====
fo = open(out_path_net, "w")
num_vertices = nx.number_of_nodes(G)

# -- vertices --
fo.write('*Vertices ' + str(num_vertices) + '\n')
for i in paj_idx:
    fo.write(ocp_space(i) + str(i) + ' \"' + label_dic[i] + '\"\n')
print('Gen Vertices List Finished.')

# -- Arcs --
if nx.is_directed(G):
    print('Graph is DIRECTED, gen Arcs...', end='')
    fo.write('*Arcs : 1 "Label of arcs relationship"\n')     # can be modified by your need.
    for i in G.edges:
        head_Pidx = label_dic_rev[i[0]]   # P_idx, pajek index of head node
        tail_Pidx = label_dic_rev[i[1]]   # P_idx, pajek index of end node
        str1 = ocp_space(head_Pidx) + str(head_Pidx)
        str2 = ocp_space(tail_Pidx) + str(tail_Pidx)
        str3 = ' ' + str(typeNo_arcs) + '\n'
        fo.write(str1 + str2 + str3)
    print('Arc list generated.')
else:
    print('Graph is UNDIRECTED, gen Edges...', end='')
    fo.write('*Edges : 2 "Label of edges relationship"\n')    # can be modified by your need.
    for i in G.edges:
        head_Pidx = label_dic_rev[i[0]]   # P_idx, pajek index of head node
        tail_Pidx = label_dic_rev[i[1]]   # P_idx, pajek index of end node
        str1 = ocp_space(head_Pidx) + str(head_Pidx)
        str2 = ocp_space(tail_Pidx) + str(tail_Pidx)
        str3 = ' ' + str(typeNo_edge) + '\n'
        fo.write(str1 + str2 + str3)
    print('Edge list generated.')
fo.close()

# ==== Gen the .clu file ====
assert os.path.exists(classes_path), 'class definition file does not exist, halted.'
classDef_dic = dict()   # node_name<string>  ->  class No.<string>
with open(classes_path, 'r') as classdefReader:
    for line in classdefReader.readlines()[1:]:
        temp_array = line.strip().split()
        classDef_dic[temp_array[0]] = temp_array[1]
classdefReader.close()   # class defining info loaded.

assert len(classDef_dic) == num_vertices, 'The number of vertices in class file does not match the edgelist!'
fo = open(out_path_clu, 'w')
fo.write('*Vertices ' + str(num_vertices) + '\n')
# .clu file is one-column file.
for idx in paj_idx:
    label = label_dic[idx]         # note: label is string, idx is int.
    classNo = classDef_dic[label]   # classNo is string
    fo.write(classNo + '\n')       # one class_No. each line
fo.close()
print('--')
print('The .net file for Pajek is generated at path=', out_path_net)
print('The .clu file for Pajek is generated at path=', out_path_clu)
