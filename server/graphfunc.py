# -*- coding: utf-8 -*-

import numpy as np
import networkx as nx
import time
import pickle
import os
import math
import datetime
from dimension2 import *
from outlier import *


def linuxtimestamp(timestr):
    timestr=timestr[:14]
    timeArray = time.strptime(timestr, "%Y%m%d%H%M%S")
    return int(time.mktime(timeArray))



class LocalGraph:
    def __init__ (self):
        self.initVars()
    def initVars(self):

        times = "20160715134955000000"
        timee = "20160716094707500000"
        self.timeset = {"starttime": linuxtimestamp(times), "curtime": linuxtimestamp(times),
                   "endtime": linuxtimestamp(timee),
                   "timestep": 60, "timewindow": 60}

        self.filepath = "../data/"
        indata = open(self.filepath + "nodesattri.pkl", 'rb')
        self.nodesattri = pickle.load(indata)
        indata.close()

        indata = open(self.filepath + "nodessps.pkl", 'rb')
        self.nodessps = pickle.load(indata)
        indata.close()

        self.G = nx.Graph()
        self.nodesselected=[]

        self.outliertype = 0
        self.outlierrecord = {}

        self.nodesattribute={}
        self.nodesappears={}
        self.spspaths={}


    def updatelocaldata(self, nodes_p,links_p):
        self.G = nx.Graph()
        for l in links_p:
            tmpsrc=l["source"]
            tmpdst=l["target"]
            tmpflow=l["flow"]
            if tmpsrc!=tmpdst:
                self.G.add_edge(tmpsrc,tmpdst,flow=tmpflow)
        for l in range(len(nodes_p)):
            self.G.nodes[nodes_p[l]['id']]['nodeType']=nodes_p[l]['nodeType']
        self.nodesattribute=nodes2highdim_update(self.G)
        # 更新outlier结果
        #self.outlierrecord = detectoutliers(self.outliertype, self.nodesattribute_pre, self.nodesattribute)

        print(self.nodesselected)
        if len(self.nodesselected) != 0:
            if len(self.nodesselected) == 1:
                return self.nodesappears
            else:
                return self.spspaths

    def nodesappear(self,nodes):
        nodesappear = {}
        for n in nodes:
            nodesappear[n] = []
            startind = 0
            for timeind in range(len(self.nodesattri[n]) - 1):
                len1 = len(self.nodesattri[n][timeind])
                len2 = len(self.nodesattri[n][timeind + 1])
                if (len1 == 0 and len2 != 0):  # start appear
                    startind = timeind + 1
                elif (len1 != 0 and len2 == 0):  # end appear
                    nodesappear[n].append([startind, timeind + 1])
        return nodesappear

    def getdim2(self,type):
        return dim2(self.nodesattribute, type)

    def getAttr(self,nodes):
        tmpattr={}
        for n in nodes:
            tmpattr[n]=self.nodesattri[n]
        nodesattr = self.getnodesattr(nodes)
        return tmpattr,nodesattr

    def choosenone(self):
        self.nodesselected=[]

    def getnodesattr(self,nodes):
        nodesattr = {}
        for n in nodes:
            nodesattr[n] = {'nodeType': self.G.nodes[n]['nodeType'], 'degree': self.G.degree(n)}
        return nodesattr

    def singlesel(self,nodes):
        self.nodesselected = nodes
        nodeid = nodes[0]
        nodesnei=list(self.G.neighbors(nodeid))
        nodesappears=self.nodesappear(nodesnei)
        nodesshown=set(nodesnei) | {nodeid}
        nodesattr = self.getnodesattr(nodesshown)
        self.nodesappears={'root': nodeid,'appear':nodesappears,'nodes':nodesattr}
        return self.nodesappears

    def mergepath(self,paths):
        if len(paths)==0:
            return []
        pathsmerged=[]
        for path in paths:
            ind=-1
            for i in range(len(pathsmerged)):
                if pathsmerged[i][0]==path:
                    ind=i
                    break
            if ind==-1:
                pathsmerged.append([path,1])
            else:
                pathsmerged[ind][1]=pathsmerged[ind][1]+1
        return pathsmerged

    def spsoverlap(self,source, target):
        availpaths = []
        for timeind in range(len(self.nodessps)):
            if type(self.nodessps[timeind]) != type(-1):
                if source in self.nodessps[timeind].keys():
                    if target in self.nodessps[timeind][source].keys():
                        availpaths.append(self.nodessps[timeind][source][target])
        availpaths = self.mergepath(availpaths)
        availpaths.sort(key=lambda d: d[1], reverse=True)
        return availpaths

    def multisel(self,nodes):
        spspaths=[]
        nodesshown=set()
        self.nodesselected = nodes
        for i in range(len(nodes)-1):
            paths=self.spsoverlap(nodes[i],nodes[i+1])
            spspaths.append(paths)
            for p in paths:
                nodesshown=nodesshown | set(p[0])
        nodesattr=self.getnodesattr(nodesshown)
        self.spspaths={'paths': spspaths,'nodes':nodesattr}
        return self.spspaths

    def getsubdata(self):
        print(self.nodesselected)
        if len(self.nodesselected)!=0:
            if len(self.nodesselected) == 1:
                return self.singlesel(self.nodesselected)
            else:
                return self.multisel(self.nodesselected)