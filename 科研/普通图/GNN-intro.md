
src:
- [distill blog](https://distill.pub/2021/gnn-intro/)

topics:
- graphs and where to find them
- what types of prob' have graph data
- the challenges of using graphs in ML
- GNN explanation

graphs are basically everything:
- text: linear graph
- image: graph with $n=w\times h$ and each pixel conn'd to their neighbors
- other types: molecules, social networks, citation networks, etc.

three levels of graph tasks: graph-level, edge-level, vtx'-level
- the objective is to predict some properties
- all levels of tasks can be resolved with GNN

*graph-level task*:
- objective: predict the property of the entire graph
- e.g. molecule classification, image classification

*node-level task*:
- objective: predict the identity or role of each node in a graph
- e.g. 
	- Zach's karate club problem: a social network where ppl' are split into two groups. the vtx's are karate players, edges are their interactions. the job is to figure out which group each person is in.
	- image segmentation
	- predicting the part-of-speech of each word in a sentence (e.g. noun, verb, adverb, etc.)

*edge-level task*:
- objective: predict the relationship of vtx's in a graph
- e.g:
	- image scene understanding: predict the relationship of objects identified in an image

*challenges of using graphs in ML*:
- difficulties in representing conn'ty: the same conn'ty may be repr'd by multiple adjacency matrices
- adjacency lists are elegant and memory-efficient

*GNN*:
