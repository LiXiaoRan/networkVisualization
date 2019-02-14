# coding=utf-8
import networkx as nx
from sklearn.manifold import TSNE
from sklearn.decomposition import KernelPCA
from sklearn.decomposition import FastICA
from sklearn.decomposition import IncrementalPCA

import time
import numpy as np
import random


def nodes2highdim_update(G):
    nodesattribute={}

    time_start = time.time()
    degrees = nx.degree_centrality(G)
    clusteringco = nx.clustering(G)
    corenum = nx.core_number(G)
    eigncenternx = nx.eigenvector_centrality_numpy(G)

    connectedG = nx.connected_components(G)
    connectednum = [c for c in connectedG]


    time_end = time.time()
    #print('get nodes attributes', time_end - time_start)

    time_start = time.time()

    nodesall = list(G.nodes())
    for n in nodesall:
        nodesattribute[n] = [degrees[n],clusteringco[n], corenum[n], eigncenternx[n], 0]
        for i in range(len(connectednum)):
            if n in connectednum[i]:
                nodesattribute[n][4] = float(len(connectednum[i]))/len(nodesall)
                break
    time_end = time.time()
    #print('update', time_end - time_start)
    return nodesattribute


def dim2(nodesattribute,type):
    nodes=list(nodesattribute.keys())
    nodesattris=np.array(list(nodesattribute.values()))
    time_start = time.time()
    nodes_embedded=[]
    if type==0:
        nodes_embedded=KernelPCA(n_components=2).fit_transform(nodesattris)
    elif type==1:
        nodes_embedded = FastICA(n_components=2).fit_transform(nodesattris)
    elif type == 2:
        nodes_embedded = TSNE(n_components=2, perplexity=30, learning_rate=100,init="pca").fit_transform(nodesattris)
    time_end = time.time()
    #print('dimension reduction', time_end - time_start)
    return nodes,nodes_embedded
