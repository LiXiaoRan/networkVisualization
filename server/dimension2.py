# coding=utf-8
import networkx as nx
from sklearn.manifold import TSNE
from sklearn.decomposition import KernelPCA
from sklearn.decomposition import FastICA
from sklearn.decomposition import IncrementalPCA

import time
import numpy as np
import random

def nodes2highdim(G):
    #初始化节点高维属性
    time_start = time.time()
    degrees = nx.degree_centrality(G)
    time_end = time.time()
    print('degree_centrality', time_end - time_start)

    time_start = time.time()
    connectedG=nx.connected_components(G)
    connectednum = [c for c in connectedG]
    time_end = time.time()
    print('connected_components', time_end - time_start)
    print('connected_components_num', len(connectednum))

    time_start = time.time()
    #eigncenter.append(nx.eigenvector_centrality_numpy(H))
    eigncenternx=nx.eigenvector_centrality_numpy(G)
    time_end = time.time()
    print('eigenvector_centrality',time_end - time_start)

    time_start = time.time()
    clusteringco = nx.clustering(G)
    time_end = time.time()
    print('clustering', time_end - time_start)

    time_start = time.time()
    corenum = nx.core_number(G)
    time_end = time.time()
    print('k_core', time_end - time_start)

    time_start = time.time()
    nodesall=list(G.nodes())
    nodesattribute={}
    for n in nodesall:
        tmpattr=[degrees[n],clusteringco[n],corenum[n],eigncenternx[n]]
        for i in range(len(connectednum)):
            if n in connectednum[i]:
                tmpattr.append(float(len(connectednum[i]))/len(nodesall))
                break
        nodesattribute[n]=tmpattr
    time_end = time.time()
    print('summary', time_end - time_start)
    return nodesattribute

def nodes2highdim_update(G,addedges,deledges,nodesattribute):
    #根据边的加减更新节点属性
    #print("f")
    time_start = time.time()
    degrees = nx.degree_centrality(G)
    time_end = time.time()
    print('degree_centrality', time_end - time_start)

    time_start = time.time()
    connectedG = nx.connected_components(G)
    connectednum = [c for c in connectedG]
    time_end = time.time()
    print('connected_components', time_end - time_start)
    print('connected_components_num', len(connectednum))

    time_start = time.time()
    # eigncenter.append(nx.eigenvector_centrality_numpy(H))
    eigncenternx = nx.eigenvector_centrality_numpy(G)
    time_end = time.time()
    print('eigenvector_centrality', time_end - time_start)

    #time_start = time.time()
    #clusteringco = nx.clustering(G)
    #time_end = time.time()
    #print('clustering', time_end - time_start)

    time_start = time.time()
    corenum = nx.core_number(G)
    time_end = time.time()
    print('k_core', time_end - time_start)

    time_start = time.time()
    nodesall = list(G.nodes())
    nodes_pre=list(nodesattribute.keys())
    #nodesattribute = {}
    for n in nodesall:
        if n in nodes_pre:
            nodesattribute[n][0] = degrees[n]
            nodesattribute[n][2] = corenum[n]
            nodesattribute[n][3] = eigncenternx[n]
        else:
            nodesattribute[n]=[degrees[n],0,corenum[n],eigncenternx[n],0]
        for i in range(len(connectednum)):
            if n in connectednum[i]:
                nodesattribute[n][4] = float(len(connectednum[i]))/len(nodesall)
                break
    '''
    for e in addedges:
        updateclustering(G, e, nodesattribute)
    for e in deledges:
        updateclustering(G, e, nodesattribute)
    '''
    updateclustering2(G, addedges, nodesattribute)

    #nodespre=nodesattribute.keys()
    for e in deledges:
        if not e[0] in nodesall and e[0] in list(nodesattribute.keys()):
            nodesattribute.pop(e[0])
        if not e[1] in nodesall and e[1] in list(nodesattribute.keys()):
            nodesattribute.pop(e[1])
    updateclustering2(G, deledges, nodesattribute)

    time_end = time.time()
    print('update', time_end - time_start)

def updateclustering2(G,edges,nodesattribute):
    #print(e[0],e[1])
    nodesupdates1=[]
    nodesupdates2=set([])
    nodes = list(G.nodes())
    for e in edges:
        if e[0] in nodes:
            nodesupdates1.append(e[0])
        if e[1] in nodes:
            nodesupdates1.append(e[1])
        if e[0] in nodes and e[1] in nodes:
            commoneneighbors = set(list(G.neighbors(e[0]))).intersection(set(list(G.neighbors(e[1]))))
            nodesupdates2=nodesupdates2 | commoneneighbors
    nodesupdates=list(set(nodesupdates1) | nodesupdates2)
    #print(nodesupdates)

    for n in nodesupdates:
        #if n in nodes:
        #print(n)
        #print("ccc",nx.clustering(G, n))
        nodesattribute[n][1] = nx.clustering(G, n)

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
    print('dimension reduction', time_end - time_start)
    return nodes,nodes_embedded
