# coding=utf-8
from igraph import *
import json


# 计算布局数据
def cal_back_layout_data(result, layout_type):
    nodes = []
    links = []

    for node in result['nodes']:
        nodes.append(node['id'])
    for link in result['links']:
        source = nodes.index(link['source'])
        target = nodes.index(link['target'])
        links.append((source, target))

    # 设置图为有向图 环状RT树布局和层次化布局不支持有向图
    if layout_type == "rt_circular" or layout_type == "sugiyama":
        graph = Graph()
    else:
        graph = Graph(directed=True)

    graph.add_vertices(len(nodes))
    graph.add_edges(links)
    lay = graph.layout(layout_type)
    in_degree_list = []
    out_degree_list = []
    if layout_type != "rt_circular" and layout_type != "sugiyama":
        in_degree_list = graph.vs.indegree()
        out_degree_list = graph.vs.outdegree()
    degree_list = graph.vs.degree()

    for i, row in enumerate(lay):
        result['nodes'][i]['x'] = row[0]
        result['nodes'][i]['y'] = row[1]
        result['nodes'][i]['degree'] = degree_list[i]
        if layout_type != "rt_circular" and layout_type != "sugiyama":
            result['nodes'][i]['in'] = in_degree_list[i]
            result['nodes'][i]['out'] = out_degree_list[i]

    for link in result['links']:
        for node in result['nodes']:
            if link['source'] == node['id']:
                link['x1'] = node['x']
                link['y1'] = node['y']
            if link['target'] == node['id']:
                link['x2'] = node['x']
                link['y2'] = node['y']

    return result
