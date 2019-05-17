# Instruction
## Motivation
The software Pajek has its own requirement for describing a graph/network. However, the `edgelist` and `adjacency matrix` may be the most intuitive way of representing a network/graph.
Moreover, it's well known that a network contains not only connection/topology information, but also attributes of components such as the features of a node or classes of a relationship.
The features/attributes of network components can be intuitively stored or organized by tables of database.
Thus, most of the information of a network can be represented by an `edgelist`/`adjacency matrix` and several `tables`.

In order to process/visualize a network with the tool `Pajek`, people need to prepare the network data as the form that can be processed by Pajek.

I looked into the wiki of Pajek and find how to convert an edgelist into .net file for Pajek. Furthermore, the tables that stores attribute of vertices can also be converted into .clu file by this code.

## The way to represent a network for Pajek
As the Pajek required, a network can be stored into several kinds of files such as: `.net`file, `.clu`file, `.vec`file, `.per`file, etc.

Below is a `.net`file example, details are described in [link](http://courses.arch.ntua.gr/fsr%2F144992/Pajek-Manual.pdf) (page 8, Figure 3)
```
*Vertices 4
  1 "Ada"                   0.1646    0.2144    0.5000
  2 "Cora"                  0.0481    0.3869    0.5000
  3 "Louise"                0.3472    0.1913    0.5000
  4 "Jean"                  0.1063    0.5935    0.5000
  < index >   < Lable >   < coordinates >
*Arcs :1 "Dining-table partner choice"
  1   3 2 
  1   2 1 
  2   1 1 
  2   4 2 
  < start >   < end >   < type of connection >
*Edges :2 "Cooperation"
  1   2 1 l "Math 2a"
  2   4 1 l "Math 2a"
  1   4 1 l "Math 2a"
  2   3 1 l "Geo 1"
```
Note: the `<...>` is comment but not the content of the `.net` file.

The `.net` file above defines the connections by Arcs(directed), and Edges(undirected) and their types(the number after the colon, `:` ) and Lables("Dining-table par...")

## How to use
Check the comments in the source code file `edgelist2pajek.py`

