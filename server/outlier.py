# coding=utf-8
from sklearn.covariance import EllipticEnvelope
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.mixture import BayesianGaussianMixture
from numpy import linalg as LA
import numpy as np
import time

def maxminvalue(nodesattr):
    tmpnodes = nodesattr.keys()
    # 提取k core num属性
    tmpcorenum = []
    for n in tmpnodes:
        tmpcorenum.append(nodesattr[n][2])
    return min(tmpcorenum),max(tmpcorenum)

def scaledattrs(min,max,originattrs):
    #对k core num属性归一化
    tmpkcore = 0
    if min != max:
        tmpkcore = float(originattrs[2] - min) / (max - min)
    tmpattrs = [originattrs[0], originattrs[1], tmpkcore, originattrs[3], originattrs[4]]
    return tmpattrs

def scaledimensions(nodesattr):
    #对k core num属性归一化
    tmpnodes=nodesattr.keys()
    standattrs=nodesattr.copy()
    #提取k core num属性
    tmpcorenum=[]
    for n in tmpnodes:
        tmpcorenum.append(nodesattr[n][2])
    #归一化
    if min(tmpcorenum)==max(tmpcorenum):
        tmpcorenum=[[0]]*len(tmpcorenum)
    else:
        minMax = MinMaxScaler()
        tmpcorenum = minMax.fit_transform(np.array(tmpcorenum).reshape(-1,1)).tolist()
    #更新standattrs
    for i in range(len(tmpnodes)):
        tmpn=tmpnodes[i]
        standattrs[tmpn]=[standattrs[tmpn][0],standattrs[tmpn][1],tmpcorenum[i][0],standattrs[tmpn][3],standattrs[tmpn][4]]
    return standattrs


def detectoutliers(type,nodesattr_pre,nodesattr_new):
    outlierrecord={}
    time_start = time.time()
    # 获取k core num最值
    mink_pre, maxk_pre = maxminvalue(nodesattr_pre)
    mink_new, maxk_new = maxminvalue(nodesattr_new)
    nodes_pre = nodesattr_pre.keys()
    nodes_new = nodesattr_new.keys()
    nodes = list(set(nodes_pre) | set(nodes_new))
    if type==0:
        #统计前后两次高维属性的差
        #nodesattr_pre=scaledimensions(nodesattr_pre0)
        #nodesattr_new=scaledimensions(nodesattr_new0)
        difference=[]
        #nodeschanged=[]
        #避免错误，全部加1，即中点（最小值）为[1,0]
        for n in nodes:
            differ=[1,0]
            if n in nodes_pre and n in nodes_new:
                tmpattrs_pre =scaledattrs(mink_pre, maxk_pre, nodesattr_pre[n])
                tmpattrs_new =scaledattrs(mink_new, maxk_new, nodesattr_new[n])
                differ[1]=LA.norm(np.array(tmpattrs_new)-np.array(tmpattrs_pre))
            elif n in nodes_pre:
                tmpattrs_pre = scaledattrs(mink_pre, maxk_pre, nodesattr_pre[n])
                differ[1] =LA.norm(np.array(tmpattrs_pre))
            elif n in nodes_new:
                tmpattrs_new = scaledattrs(mink_new, maxk_new, nodesattr_new[n])
                differ[1] =LA.norm(np.array(tmpattrs_new))
            if differ[1]==0:
                differ[1]=0.0001
            difference.append(differ)
        difference=np.array(difference)
        # 阈值，设一个度为1的节点消失产生的属性差为differ，阈值设为differ*1.5，小于阈值的异常不计
        mindegree=float(1)/len(nodes_pre)
        threshold=0
        for n in nodes_pre:
            if nodesattr_pre[n][0]<mindegree*1.1:
                tmpattrs_pre = scaledattrs(mink_pre, maxk_pre, nodesattr_pre[n])
                threshold=LA.norm(np.array(tmpattrs_pre))
                break
        threshold=threshold*1.5
        #检测outlier
        dectector = EllipticEnvelope(contamination=0.1)
        results=dectector.fit(difference).predict(difference)
        #更新outlier记录
        recordnodes=outlierrecord.keys()
        for i in range(len(results)):
            if results[i]==-1:
                if difference[i][1]>threshold:
                    outlierrecord[nodes[i]] = difference[i][1]
                    '''
                    #记录每个节点为outlier的次数
                    if nodes[i] in recordnodes:
                        outlierrecord[nodes[i]]=outlierrecord[nodes[i]]+1
                    else:
                        outlierrecord[nodes[i]]=1
                    '''
    else:
        #只对前后都出现的节点聚类
        nodes_together = list(set(nodes_pre) & set(nodes_new))
        #k core num归一化，提取value
        nodesval_pre=[]
        nodesval_new=[]
        for i in range(len(nodes_together)):
            n=nodes_together[i]
            nodesval_pre.append(scaledattrs(mink_pre, maxk_pre, nodesattr_pre[n]))
            nodesval_new.append(scaledattrs(mink_new, maxk_new, nodesattr_new[n]))
        '''for i in range(len(nodes_pre)):
            n=nodes_pre[i]
            nodesval_pre[n] = scaledattrs(mink_pre, maxk_pre, nodesattr_pre[n])
        for i in range(len(nodes_new)):
            n = nodes_new[i]
            nodesval_new[n] = scaledattrs(mink_new, maxk_new, nodesattr_new[n])'''
        nodesval_pre=np.array(nodesval_pre)
        nodesval_new=np.array(nodesval_new)
        #聚类
        class_pre=BayesianGaussianMixture(n_components=6,n_init=3).fit(nodesval_pre).predict(nodesval_pre)
        class_new=BayesianGaussianMixture(n_components=6,n_init=3).fit(nodesval_new).predict(nodesval_new)
        #类分裂
        visited_class=[]
        for c in class_pre:
            #对每个前一次类别，获取该类别节点在最新一次聚类中的类别
            if not c in visited_class:
                visited_class.append(c)
                nodesindex=np.where(class_pre==c)[0]
                newclass=[]
                for id in nodesindex:
                    newclass.append(class_new[id])
                newclass=np.array(newclass)
                uniqnewclass=np.array(list(set(newclass)))
                # 如果不再是同一类
                if len(uniqnewclass)!=1:
                    for cnew in uniqnewclass:
                        tmpnodesid=np.where(newclass==cnew)[0]
                        # 如果有30%节点一起分为了另一类，不属于异常（如：原本同属于一个类的8个节点变成了4个节点各属于一类），否则认为是异常
                        if not(len(tmpnodesid)>0.3*len(nodesindex)):
                            for id2 in tmpnodesid:
                                tmpnode=nodes_together[nodesindex[id2]]
                                outlierrecord[tmpnode] = 1-float(len(tmpnodesid))/len(nodesindex)
        '''
        #类合并
        visited_class = []
        for c in class_new:
            if not c in visited_class:
                visited_class.append(c)
                nodesindex = np.where(class_new == c)[0]
                preclass = []
                for id in nodesindex:
                    preclass.append(class_pre[id])
                preclass = np.array(preclass)
                uniqpreclass = np.array(list(set(preclass)))
                if len(uniqpreclass) != 1:
                    for cpre in uniqpreclass:
                        tmpnodesid = np.where(preclass == cpre)[0]
                        if not (len(tmpnodesid) > 0.3 * len(nodesindex)):
                            for id2 in tmpnodesid:
                                tmpnode = nodes_together[nodesindex[id2]]
                                tmpabnormal=1 - float(len(tmpnodesid)) / len(nodesindex)
                                if not(tmpnode in outlierrecord.keys()) or (tmpnode in outlierrecord.keys() and outlierrecord[tmpnode]<tmpabnormal):
                                    outlierrecord[tmpnode] = tmpabnormal
        '''
    time_end = time.time()
    print('detect outliers', time_end - time_start)
    return outlierrecord


if __name__ == '__main__':
    print("a")
