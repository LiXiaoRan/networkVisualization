# coding=utf-8
import networkx as nx
import numpy as np
from collections import Counter


def remove_list(target, source):
    all_nodes = list(target)  # 转变为列表
    for item in source:  # 移除指定的节点
        all_nodes.remove(item)
    return all_nodes


# 将数据处理为力导向图可以使用的格式
def handleData(result):
    nodes = []  # 取出所有的节点
    for i, val in enumerate(result['nodes']):
        nodes.append(val['id'])
    for i, val in enumerate(result['links']):
        target = val['target']
        source = val['source']
        i = 0
        for i2, val2 in enumerate(nodes):
            if (target == val2):
                i += 1
                val['target'] = i2
            if (val2 == source):
                i += 1
                val['source'] = i2
            if (i == 2):  # 两个都找到了退出
                break


def get_group(community, nodes):
    for i2, val2 in enumerate(community):
        for i, val in enumerate(nodes):
            if val['id'] in val2:
                val['group'] = i2


# 比较函数cmp
def numeric_compare(x, y):
    return int(x) - int(y)


def getListLink(G, path_list_name):
    pairs = []
    for (index, item) in enumerate(path_list_name):
        if index == len(path_list_name) - 1:
            break
        pairs.append(G.edges[path_list_name[index], path_list_name[index + 1]]['id'])
    return pairs


def numeric_compare(x, y):
    return int(x) - int(y)


def find_max_degree(graph):
    lists = nx.classes.function.degree(graph)
    max_degree = 0
    for n, degree in lists:
        if degree > max_degree:
            max_degree = degree
    return max_degree


def find_number_of_nodes(graph):
    return nx.classes.function.number_of_nodes(graph)


def find_number_of_edges(graph):
    return nx.classes.function.number_of_edges(graph)


def find_max_degree(graph):
    actual_degrees = [d for v, d in graph.degree()]
    max_degree = max(actual_degrees)
    return max_degree


def find_min_degree(graph):
    actual_degrees = [d for v, d in graph.degree()]
    min_degree = min(actual_degrees)
    return min_degree


def sort_degree(graph):
    actual_degrees = sorted([d for v, d in graph.degree()])
    return actual_degrees


def find_arrange_degree(li):
    con = set(li)
    # con.remove(max(li))
    # con.remove(min(li))
    return len(con)


def numeric_compare(x, y):
    return int(x) - int(y)


def counter(arr):
    """获取每个元素的出现次数，使用标准库collections中的Counter方法"""
    return Counter(arr).most_common(2)  # 返回出现频率最高的两个数


def single_list(arr, target):
    """获取单个元素的出现次数，使用list中的count方法"""
    return arr.count(target)


def all_list(arr):
    """获取所有元素的出现次数，使用list中的count方法"""
    result = {}
    for i in set(arr):
        result[i] = arr.count(i)
    return result


def single_np(arr, target):
    """获取单个元素的出现次数，使用Numpy"""
    arr = np.array(arr)
    mask = (arr == target)
    arr_new = arr[mask]
    return arr_new.size


def all_np(arr):
    """获取每个元素的出现次数，使用Numpy"""
    arr = np.array(arr)
    key = np.unique(arr)
    result = {}
    for k in key:
        mask = (arr == k)
        arr_new = arr[mask]
        v = arr_new.size
        result[k] = v
    return result


def find_max_degree(graph):
    lists = nx.classes.function.degree(graph)
    max_degree = 0
    for n, degree in lists:
        if degree > max_degree:
            max_degree = degree
    return max_degree


def parallel(choose_subgraph, sub_g, G):
    edge_id_list = []
    subgraph = G.subgraph(choose_subgraph)
    if nx.algorithms.isomorphism.is_isomorphic(subgraph, sub_g):
        for item in list(subgraph.edges):
            edge_id_list.append(G[item[0]][item[1]])
    return edge_id_list
