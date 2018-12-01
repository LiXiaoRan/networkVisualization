#coding=utf-8
import networkx as nx
import functools
import operator
#from readdata import *
from bitarray import bitarray
import time


def enQ(queue,ele):
    queue.append(ele)
def deQ(queue):
    if len(queue) == 0:
        return -1
    else:
        return queue.pop(0)
def viewQ(queue):
    print(queue)

def search_next(qs,G,Ps,Pt,ds,ignorenodes):
    #判断队列中的节点的邻居节点是否在另一个BFS中被访问过了
    #如果是，说明找到了两个BFS的交叉节点，即最短路径，返回所有可能的交叉节点
    qs_next=[]#下一层要访问的节点列表
    qlen=len(qs)
    hopnodes=[]#记录交叉节点
    for i in range(qlen):
        v=deQ(qs)
        tmpchilds=[]
        for w in G.neighbors(v):
            if w in ignorenodes:
                continue
            #如果这个邻居节点w没有作为父节点被BFS访问过，加入qs_next，下一次BFS时访问
            if (w not in list(Ps.keys())):
                tmpchilds.append(w)
                if w not in qs_next:
                    enQ(qs_next,w)
            #如果w在另一个BFS中被访问过了，而且不是已知的交叉节点，那么说明w也是交叉节点
            if (w in sum(list(Pt.values()), [])) and (w not in hopnodes):
                hopnodes.append(w)
        #更新该BFS访问过的节点记录
        if len(tmpchilds)!=0:
            Ps[v]=tmpchilds
    if len(hopnodes)!=0:
        return 1, qs, ds, hopnodes
        #找到了最短路径，qs，ds，交叉节点
    else:
        qs=qs_next
        return -1,qs,ds+1,-1
        # 没有找到最短路径，新的队列，新的距离，-1

def getpath0(s,P,t,i,maxnum):
    #根据访问过的节点记录P，迭代求s到t的路径
    #i记录迭代次数，maxnum表示最大距离
    #超过最大距离，说明不可能是最短路径
    if i>maxnum+1:
        return -1
    #迭代结束
    if s==t:
        return [[s]]
    #找t的所有父节点
    t_parents = []
    for k in list(P.keys()):
        if t in P[k]:
            t_parents.append(k)
    paths=[]
    for k in range(len(t_parents)):
        #迭代求s到t的父节点的路径
        newpaths=getpath0(s,P,t_parents[k],i+1,maxnum)
        #合并路径
        if newpaths!=-1:
            for j in range(len(newpaths)):
                paths.append([t]+newpaths[j])

    return paths

def getpath(s,t,Ps,Pt,ds,dt,hopnode):
    path1=getpath0(s, Ps, hopnode, 0, ds)
    for i in range(len(path1)):
        path1[i].reverse()
        path1[i].pop()
    #print("path1",path1)
    path2 = getpath0(t, Pt, hopnode, 0, dt)
    #print("path2", path2)
    path=[]
    for i in range(len(path1)):
        for j in range(len(path2)):
            path.append(path1[i]+path2[j])
    return path

def biBFS(G,s,t,ignorenodes):
    #双向BFS
    #在图G中寻找s到t的所有最短路径
    #返回二维list
    Qs=[s]#从s开始的正向BFS的队列
    Qt=[t]#从t开始的反向BFS的队列
    Ps={s:[t]}#从s开始访问过的节点
    Pt={t:[t]}
    ds=0#从s开始BFS的当前距离
    dt=0
    paths=[]
    '''
    #计算上界
    dmin=100000
    for r in SPTs:
        if (s in r) and (t in r):
            if r[s]+r[t]<dmin:
                dmin=r[s]+r[t]
    '''
    while not(len(Qs)==0 or len(Qt)==0):
        #正向反向BFS交替执行
        if len(sum(list(Ps.values()), []))<=len(sum(list(Pt.values()), [])):
            found,Qs,ds,hopnodes = search_next(Qs, G, Ps, Pt, ds,ignorenodes)
            #print("Qs",Qs)
            #print("Ps",Ps)
            #print("ds",ds)
            #print("\n")
        else:
            found,Qt,dt,hopnodes = search_next(Qt, G, Pt, Ps, dt,ignorenodes)
            #print("Qt", Qt)
            #print("Pt", Pt)
            #print("dt", dt)
            #print("\n")
        if found==1:
            for hopnode in hopnodes:
                path=getpath(s, t, Ps, Pt,ds,dt, hopnode)
                for p in path:
                    paths.append(p)
            #print("min distance: ",ds+dt+1)
    return paths


def initBFStree(G,nodeid):
    treeinfo={}
    nodesarr=[]
    #treeinfo["rootid"]=nodeid
    #ET=[]
    VT=[nodeid]
    Thislevel=[nodeid]
    curlevel=0
    while len(Thislevel)!=0:
        Nextlevel=[]
        for x in Thislevel:
            treeinfo[x]={}
            nodesarr.append(x)
            neighborsxy=list(G.neighbors(x))
            neighborsxy.sort()
            #print(neighborsxy)
            treeinfo[x]["fs"]=neighborsxy
            chx=[]
            for y in neighborsxy:
                if not y in VT:
                    #ET.append([x,y])
                    VT.append(y)
                    Nextlevel.append(y)
                    chx.append(y)
            treeinfo[x]["d"]=curlevel
            treeinfo[x]["ch"]=chx

        curlevel=curlevel+1
        Thislevel=Nextlevel
        #time_start = time.time()
        Thislevel.sort()
        #time_end = time.time()
        #print('sort ', time_end-time_start)

    for k in list(treeinfo.keys()):
        for ch in treeinfo[k]["ch"]:
            treeinfo[ch]["p"]=k
    nodesarr.sort()
    treeinfo={"rootid":nodeid,"bfstree":treeinfo,"nodes":nodesarr}

    return treeinfo

def propagate(treeinfo,edgesset):
    while len(edgesset)!=0:
        # let <a1,b1> be an edge in L having minimum d(a1)+1
        a1=edgesset[0][0]
        b1=edgesset[0][1]
        mind=treeinfo["bfstree"][a1]["d"]
        for [a,b] in edgesset:
            tmpd=treeinfo["bfstree"][a]["d"]
            # select <a,b> from L s.t. d(a)=d(a1) and a has minimum rank
            if tmpd<mind or (tmpd==mind and a<a1):
                a1=a
                b1=b
                mind=tmpd
        #remove all edges <a2,b> from L
        edgesset_new=[]
        for e in edgesset:
            if e[1]!=b1:
                edgesset_new.append(e)
        edgesset=edgesset_new
        treeinfo["bfstree"][b1]["p"]=a1
        if treeinfo["bfstree"][b1]["d"]>treeinfo["bfstree"][a1]["d"]+1:
            treeinfo["bfstree"][b1]["d"] = treeinfo["bfstree"][a1]["d"] + 1
            for fsnode in treeinfo["bfstree"][b1]["fs"]:
                if (treeinfo["bfstree"][fsnode]["d"]>treeinfo["bfstree"][b1]["d"]+1) or \
                    (treeinfo["bfstree"][fsnode]["d"]==treeinfo["bfstree"][b1]["d"]+1 and b1<treeinfo["bfstree"][fsnode]["p"]):
                    edgesset.append([b1,fsnode])
        #print(edgesset)
def updatechildnodes(treeinfo):
    #update ch
    for node in treeinfo["nodes"]:
        treeinfo["bfstree"][node]["ch"]=[]
    for node in treeinfo["nodes"]:
        if node!=treeinfo["rootid"]:
            tmpp=treeinfo["bfstree"][node]["p"]
            treeinfo["bfstree"][tmpp]["ch"].append(node)
    #return 1


def insertEdge_BFS(treeinfo,edge):
    nodes=treeinfo["nodes"]
    x=edge[0]
    y=edge[1]
    #如果插入的边（两个节点）和原来的bfs无关，直接返回
    if (not x in nodes) and (not y in nodes):
        return treeinfo
    #如果只有一个节点是新加入的，直接扩展bfs tree
    if not x in nodes:
        treeinfo["bfstree"][y]["ch"].append(x)
        treeinfo["bfstree"][y]["ch"].sort()
        treeinfo["bfstree"][y]["fs"].append(x)
        treeinfo["bfstree"][y]["fs"].sort()
        treeinfo["bfstree"][x]={"p":y,"ch":[],"d":treeinfo["bfstree"][y]["d"]+1,"fs":[y]}
        treeinfo["nodes"].append(x)
        treeinfo["nodes"].sort()
        return treeinfo
    if not y in nodes:
        treeinfo["bfstree"][x]["ch"].append(y)
        treeinfo["bfstree"][x]["ch"].sort()
        treeinfo["bfstree"][x]["fs"].append(y)
        treeinfo["bfstree"][x]["fs"].sort()
        treeinfo["bfstree"][y]={"p":x,"ch":[],"d":treeinfo["bfstree"][x]["d"]+1,"fs":[x]}
        treeinfo["nodes"].append(y)
        treeinfo["nodes"].sort()
        return treeinfo
    #如果两个节点都在原来的bfs tree中
    #由于是无向图，保持 d 较大的节点为y
    if treeinfo["bfstree"][y]["d"]<treeinfo["bfstree"][x]["d"]:
        tmpid=x
        x = y
        y=tmpid
    treeinfo["bfstree"][x]["fs"].append(y)
    treeinfo["bfstree"][x]["fs"].sort()
    treeinfo["bfstree"][y]["fs"].append(x)
    treeinfo["bfstree"][y]["fs"].sort()
    if (treeinfo["bfstree"][y]["d"]>treeinfo["bfstree"][x]["d"]+1) or (treeinfo["bfstree"][y]["d"]==treeinfo["bfstree"][x]["d"]+1 and x<treeinfo["bfstree"][y]["p"]):
        propagate(treeinfo,[[x,y]])
    updatechildnodes(treeinfo)
    return treeinfo

def deleteEdge_BFS(treeinfo,edge):
    nodes = treeinfo["nodes"]
    x = edge[0]
    y = edge[1]
    # 如果删除的边和原来的bfs无关，直接返回
    if (not x in nodes) or (not y in nodes):
        return treeinfo
    # 由于是无向图，保持 d 较大的节点为y
    if treeinfo["bfstree"][y]["d"] < treeinfo["bfstree"][x]["d"]:
        tmpid = x
        x = y
        y = tmpid
    # 如果删除后导致孤立点
    if treeinfo["bfstree"][y]["p"]==x and len(treeinfo["bfstree"][y]["fs"])==1:
        treeinfo["bfstree"].pop(y)
        treeinfo["nodes"].remove(y)
        treeinfo["bfstree"][x]["fs"].remove(y)
        treeinfo["bfstree"][x]["ch"].remove(y)
        return treeinfo
    #x和y均在原来的bfs中
    treeinfo["bfstree"][x]["fs"].remove(y)
    treeinfo["bfstree"][y]["fs"].remove(x)
    if treeinfo["bfstree"][y]["p"]==x:
        tmpp=treeinfo["bfstree"][y]["fs"][0]
        tmppd=treeinfo["bfstree"][tmpp]["d"]
        for n in treeinfo["bfstree"][y]["fs"]:
            if treeinfo["bfstree"][n]["d"]<tmppd:
                tmppd=treeinfo["bfstree"][n]["d"]
                tmpp=n
            if treeinfo["bfstree"][n]["d"]==tmppd and n<tmpp:
                tmpp=n
        treeinfo["bfstree"][y]["p"]=tmpp
        treeinfo["bfstree"][y]["d"]=treeinfo["bfstree"][tmpp]["d"]+1

        R_bar=[]
        nodes_next=treeinfo["bfstree"][y]["ch"]
        #for each vertex b in S(y), scanned by increasing tree level
        while len(nodes_next)!=0:
            #print(nodes_next)
            new_nodes=[]
            for b in nodes_next:
                for newn in treeinfo["bfstree"][b]["ch"]:
                    if not newn in new_nodes:
                        new_nodes.append(newn)
                find_flag=0
                for a in treeinfo["bfstree"][b]["fs"]:
                    if treeinfo["bfstree"][a]["d"]+1==treeinfo["bfstree"][b]["d"]: #and (a!=y or treeinfo["bfstree"][y]["p"]!=b):
                        find_flag = 1
                        treeinfo["bfstree"][b]["p"]=a
                        break
                if find_flag==0:
                    treeinfo["bfstree"][b]["d"] = float("inf")
                    R_bar.append(b)
            nodes_next=new_nodes
        #print(R_bar)
        if len(R_bar)!=0:
            L=[]
            for b in R_bar:
                mind_a=treeinfo["bfstree"][b]["fs"][0]
                mind=treeinfo["bfstree"][mind_a]["d"]
                for a in treeinfo["bfstree"][b]["fs"]:
                    tmpd=treeinfo["bfstree"][a]["d"]
                    if tmpd<mind:
                        mind_a=a
                        mind=tmpd
                if mind!=float("inf"):
                    L.append([mind_a,b])
            propagate(treeinfo, L)

        tmpp = treeinfo["bfstree"][y]["fs"][0]
        tmppd = treeinfo["bfstree"][tmpp]["d"]
        for n in treeinfo["bfstree"][y]["fs"]:
            if treeinfo["bfstree"][n]["d"] < tmppd:
                tmppd = treeinfo["bfstree"][n]["d"]
                tmpp = n
            if treeinfo["bfstree"][n]["d"] == tmppd and n < tmpp:
                tmpp = n
        treeinfo["bfstree"][y]["p"] = tmpp
        treeinfo["bfstree"][y]["d"] = treeinfo["bfstree"][tmpp]["d"] + 1
    updatechildnodes(treeinfo)
    return treeinfo



