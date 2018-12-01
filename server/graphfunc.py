# -*- coding: utf-8 -*-

import numpy as np
import networkx as nx
from dimension2 import *
from outlier import *
from dynamicBFS import *

class LocalGraph:
    def __init__ (self):
        self.initVars()
    def initVars(self):
        self.startnum = 0
        self.updatenum = 0
        self.updatestep = 1

        self.G = nx.Graph()
        #self.none0tree1sub2=0
        self.nodesselected=[]
        self.treeinfo = {"rootid": -1, "bfstree": {}, "nodes": []}

        self.nodesattribute = {}
        self.nodesattribute_pre = {}

        self.outliertype = 0
        self.outlierrecord = {}

        self.remain_edges = []
        self.nodes_degree = {}  # {nodeid:{timestamp1:x1,timestamp2:x2},...}
        self.nodes_clustering = {}
        self.nodes_kcore = {}
        self.nodes_eigen = {}
        self.nodes_reachable = {}

        self.add_edges = []
        self.del_edges = []

    def initgraph(self):
        # 初始化节点高维属性
        # 更新节点degree属性
        tmpnodes = list(self.G.nodes())
        for n in tmpnodes:
            self.nodes_degree[n] = {self.startnum: 0}
            self.nodes_clustering[n] = {self.startnum: 0}
            self.nodes_kcore[n] = {self.startnum: 0}
            self.nodes_eigen[n] = {self.startnum: 0}
            self.nodes_reachable[n] = {self.startnum: 0}
        edges = list(self.G.edges())
        for (a, b) in edges:
            self.nodes_degree[a][self.startnum] = self.nodes_degree[a][self.startnum] + 1
            self.nodes_degree[b][self.startnum] = self.nodes_degree[b][self.startnum] + 1
        for n in self.nodes_degree:
            # 度为零，孤立点，去除
            if self.nodes_degree[n][self.startnum] == 0:
                self.G.remove_node(n)
        # 获取节点其他属性
        self.nodesattribute = nodes2highdim(self.G)
        self.nodesattribute_pre = self.nodesattribute.copy()
        # 更新节点其他属性
        tmpnodes = list(self.G.nodes())
        for n in tmpnodes:
            self.nodes_clustering[n] = {self.startnum: self.nodesattribute[n][1]}
            self.nodes_kcore[n] = {self.startnum: self.nodesattribute[n][2]}
            self.nodes_eigen[n] = {self.startnum: self.nodesattribute[n][3]}
            self.nodes_reachable[n] = {self.startnum: self.nodesattribute[n][4]}

    def getupdatededges(self, linksnew):
        # 获取旧graph->新graph的增加边和删除边
        links = list(self.G.edges())
        addedges = [val for val in linksnew if val not in links]
        deledges = [val for val in links if val not in linksnew]
        return addedges, deledges

    def updateG(self,addedges, deledges, lasttime, newtime):
        #更新G和degree记录
        global G,nodes_degree
        for n in list(self.nodes_degree.keys()):
            self.nodes_degree[n][newtime] = self.nodes_degree[n][lasttime]
        for (a, b) in addedges:
            if not a in list(self.nodes_degree.keys()):
                self.nodes_degree[a] = {newtime: 0}
            if not b in list(self.nodes_degree.keys()):
                self.nodes_degree[b] = {newtime: 0}
            self.nodes_degree[a][newtime] = self.nodes_degree[a][newtime] + 1
            self.nodes_degree[b][newtime] = self.nodes_degree[b][newtime] + 1
            self.G.add_edge(a, b)
        for (a, b) in deledges:
            self.nodes_degree[a][newtime] = self.nodes_degree[a][newtime] - 1
            self.nodes_degree[b][newtime] = self.nodes_degree[b][newtime] - 1
            self.G.remove_edge(a, b)
        nodes=list(self.G.nodes())
        for n in self.nodes_degree:
            #度为零，孤立点，去除
            if self.nodes_degree[n][newtime]==0 and n in nodes:
                self.G.remove_node(n)

    def updateattributes(self,newtime):
        # 更新degree记之外的其他属性记录
        prenodes = list(self.nodes_clustering.keys())
        newnodes = list(self.nodesattribute.keys())
        tmpnodes = list(set(prenodes) | set(newnodes))
        for n in tmpnodes:
            if n in prenodes and n in newnodes:
                self.nodes_clustering[n][newtime] = self.nodesattribute[n][1]
                self.nodes_kcore[n][newtime] = self.nodesattribute[n][2]
                self.nodes_eigen[n][newtime] = self.nodesattribute[n][3]
                self.nodes_reachable[n][newtime] = self.nodesattribute[n][4]
            elif n in newnodes:
                # 之前从未出现过的节点
                self.nodes_clustering[n] = {newtime: 0}
                self.nodes_kcore[n] = {newtime: 0}
                self.nodes_eigen[n] = {newtime: 0}
                self.nodes_reachable[n] = {newtime: 0}
            elif n in prenodes:
                # 消失的节点
                self.nodes_clustering[n][newtime] = 0
                self.nodes_kcore[n][newtime] = 0
                self.nodes_eigen[n][newtime] = 0
                self.nodes_reachable[n][newtime] = 0

    def updatelocaldata(self, igraphobj, calltimes):
        linksnew = igraphobj.get_edgelist()
        linksnew = list(set(linksnew))
        if calltimes==0:
            self.initVars()
            self.G=nx.Graph(linksnew)
            self.G.remove_edges_from(self.G.selfloop_edges())
            self.initgraph()
        else:
            self.add_edges,self.del_edges=self.getupdatededges(linksnew)
            # 更新graph和degree记录
            self.updateG(self.add_edges, self.del_edges, self.startnum + (self.updatenum) * self.updatestep, self.startnum + (self.updatenum + 1) * self.updatestep)
            self.G.remove_edges_from(self.G.selfloop_edges())
            # 更新节点高维属性
            self.nodesattribute_pre = self.nodesattribute.copy()
            nodes2highdim_update(self.G, self.add_edges, self.del_edges, self.nodesattribute)
            # 更新outlier结果
            self.outlierrecord = detectoutliers(self.outliertype, self.nodesattribute_pre, self.nodesattribute)
            # 更新degree以外的记录
            self.updateattributes(self.startnum + (self.updatenum+1) * self.updatestep)

            self.updatenum = self.updatenum + 1
            print(self.nodesselected)
            if len(self.nodesselected) != 0:
                if len(self.nodesselected) == 1:
                    for e in self.add_edges:
                        insertEdge_BFS(self.treeinfo, e)
                    for e in self.del_edges:
                        deleteEdge_BFS(self.treeinfo, e)
                    # return {'nodes': list(self.G.nodes()), 'edges': list(self.G.edges()), 'treeinfo': self.treeinfo}
                    return {'treeinfo': self.treeinfo}
                elif len(self.nodesselected) == 2:
                    paths = biBFS(self.G, self.nodesselected[0], self.nodesselected[1], [])
                    # return {'nodes': list(self.G.nodes()), 'edges': list(self.G.edges()), 'paths': paths}
                    return {'paths': paths}
                else:
                    subgraph = self.G.subgraph(self.nodesselected)
                    # return {'nodes': list(self.G.nodes()), 'edges': list(self.G.edges()),'subgraph_nodes': list(subgraph.nodes()), 'subgraph_edges': list(subgraph.edges())}
                    return {'subgraph_nodes': list(subgraph.nodes()), 'subgraph_edges': list(subgraph.edges())}

    def getdim2(self,type):
        return dim2(self.nodesattribute, type)
    def getAttr(self,type,nodes):
        tmpattrall = [self.nodes_degree, self.nodes_clustering, self.nodes_kcore, self.nodes_eigen, self.nodes_reachable]
        tmpattr = {}
        for n in nodes:
            tmpattr[n] = tmpattrall[type][n]
        return tmpattr

    def choosenone(self):
        self.nodesselected=[]
    def getBFStree(self,nodes):
        self.nodesselected = nodes
        print(self.nodesselected)
        nodeid=nodes[0]
        if self.treeinfo["rootid"] != nodeid:
            self.treeinfo = initBFStree(self.G, nodeid)
        return {'treeinfo': self.treeinfo}
    def getSPs(self, nodes):
        self.nodesselected = nodes
        node1 = nodes[0]
        node2 = nodes[1]
        paths = biBFS(self.G, node1, node2, [])
        return {'paths': paths}
    def getSubgraph(self,nodes):
        self.nodesselected = nodes
        subgraph = self.G.subgraph(nodes)
        return {'subgraph_nodes': list(subgraph.nodes()),
                        'subgraph_edges': list(subgraph.edges())}

    def getsubdata(self):
        print(self.nodesselected)
        if len(self.nodesselected)!=0:
            if len(self.nodesselected) == 1:
                return self.getBFStree(self.nodesselected)
            elif(len(self.nodesselected) == 2):
                return self.getSPs(self.nodesselected)
            else:
                return self.getSubgraph(self.nodesselected)