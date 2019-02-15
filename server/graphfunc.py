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

        self.rangestart=0
        self.rangeend=0


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

        #print(self.nodesselected)
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
        nodes,nodes_embedded=dim2(self.nodesattribute, type)
        nodes_embedded=nodes_embedded.tolist()
        tmpobj={}
        for i in range(len(nodes)):
            n=nodes[i]
            tmpobj[n]={
                'nodeType': self.G.nodes[n]['nodeType'],
                 'embedded':nodes_embedded[i]
            }
        return tmpobj

    def getAttr(self,nodes):
        tmpattr={}
        attrnum=5
        for n in nodes:
            tmpattr[n]=self.nodesattri[n]
            '''
            for t in range(len(tmpattr[n])):
                if len(tmpattr[n][t])==0:
                    tmpattr[n][t]=np.array([0]*attrnum).tolist()
                else:
                    tmpattr[n][t] = np.array(tmpattr[n][t]).tolist()
            tmpattr[n] = np.array(tmpattr[n])
            tmpattr[n]=np.transpose(tmpattr[n]).tolist()
            '''
        nodesattr = self.getnodesattr(nodes)
        return tmpattr,nodesattr

    def choosenone(self):
        self.nodesselected=[]

    def getnodesattr(self,nodes):
        nodesattr = {}
        for n in nodes:
            #nodesattr[n] = {'nodeType': self.G.nodes[n]['nodeType'], 'degree': self.G.degree(n)}
            nodesattr[n] = {'nodeType': self.G.nodes[n]['nodeType']}
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


    def getspshist(self,source, target):
        timeindstart = int(math.ceil(float(self.rangestart-self.timeset["starttime"])/self.timeset["timestep"]))
        timeindend = int(math.ceil(float(self.rangeend-self.timeset["starttime"])/self.timeset["timestep"]))

        try:
            cursps = [p for p in nx.all_shortest_paths(self.G, source=source, target=target)]
            curspsrecord = []
            for i in range(len(cursps)):
                curspsrecord.append([])
                cursp = cursps[i]
                for nodeind in range(len(cursp) - 1):
                    curspsrecord[i].append([-1] * (timeindend - timeindstart))

                for timeind in range(timeindend-timeindstart):
                    tmpspsall = self.nodessps[timeind]
                    if type(tmpspsall)==type(-1):
                        continue
                    if source in tmpspsall.keys():
                        if target in tmpspsall[source].keys():
                            tmpsps = tmpspsall[source][target]
                            for spind in range(len(tmpsps)):
                                tmpsp = tmpsps[spind]
                                for nodeind in range(len(cursp) - 1):
                                    curnode1 = cursp[nodeind]
                                    curnode2 = cursp[nodeind + 1]

                                    for nodeind2 in range(len(tmpsp) - 1):
                                        if tmpsp[nodeind2] == curnode1 and tmpsp[nodeind2 + 1] == curnode2:
                                            curspsrecord[i][nodeind][timeind] = 1
                                            continue
            return cursps,curspsrecord
        except nx.exception.NetworkXNoPath:
            return [[source,target]],[[-1] * (timeindend - timeindstart)]

    def multisel(self,nodes):
        spspaths=[]
        spspathsrecord=[]
        nodesshown=[]
        self.nodesselected = nodes
        for i in range(len(nodes)-1):
            paths,pathsrecord=self.getspshist(nodes[i],nodes[i+1])
            spspaths.append(paths)
            spspathsrecord.append(pathsrecord)
            for p in paths:
                #nodesshown=nodesshown | set(p[0])
                for n in p:
                    nodesshown.append(n)
        nodesshown=list(set(nodesshown))
        nodesattr=self.getnodesattr(nodesshown)
        self.spspaths={'paths': spspaths,'nodes':nodesattr,'records':spspathsrecord}
        return self.spspaths

    def getsubdata(self):
        #print(self.nodesselected)
        if len(self.nodesselected)!=0:
            if len(self.nodesselected) == 1:
                return self.singlesel(self.nodesselected)
            else:
                return self.multisel(self.nodesselected)