# -*- coding: utf-8 -*-
import requests
import time
import random
import json
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
import os
import sys
import database
from tornado.options import define, options
import tornado.websocket
import datetime
import igraphLayout
import graphfunc
import networkx as nx
import json
import numpy as np
import math
import codecs
import copy

define("port", default=22333, type=int, help="run on the given port")
client_file_root_path = os.path.join(os.path.split(__file__)[0], '../')
client_file_root_path = os.path.abspath(client_file_root_path)

NetworkData = database.NetworkData()
LocalGraph = graphfunc.LocalGraph()


class getRecentDataHandler(tornado.web.RequestHandler):
    def post(self):
        self.set_header('Access-Control-Allow-Origin',
                        '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods",
                        "PUT,POST,GET,DELETE,OPTIONS")

    def get(self):
        # 时间轴获取统计数据
        self.set_header('Access-Control-Allow-Origin',
                        '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods",
                        "PUT,POST,GET,DELETE,OPTIONS")
        params = self.get_argument('params')
        params = json.loads(params)
        data = NetworkData.getDataByRecentTime(params)
        self.write({'data': data})


class getLayoutData(tornado.web.RequestHandler):
    # 计算前端选择布局后提交的数据
    def get(self):
        print("进入get")
        self.set_header('Access-Control-Allow-Origin',
                        '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods",
                        "PUT,POST,GET,DELETE,OPTIONS")
        params = self.get_argument('params')
        params = json.loads(params)
        layoutType = params['layout_type']
        networkLevel = int(params['network_level'])
        data = []
        if networkLevel != 0:
            startLevel = networkLevel * 100
            endLevel = startLevel + 100
            for item in nowSelectedData:
                if startLevel <= int(item['net_level']) < endLevel:
                    data.append(item)
        else:
            data = copy.deepcopy(nowSelectedData)
        if len(data):
            links = []
            temp_nodes = []
            nodes = []
            nodes_id = []
            start = time.clock()
            for row in data:
                source = row['trans_node_global_no']
                source_type = row['trans_node_type']
                source_palsy = row['trans_palsy_level']
                source_control = row['trans_control_level']
                target = row['recv_node_golbal_no']
                target_type = row['recv_node_type']
                target_palsy = row['recv_palsy_level']
                target_control = row['recv_control_level']
                flow = row['flow']
                link = {'source': source, 'target': target, 'flow': flow}
                temp_nodes.append({
                    'id': source,
                    'nodeType': source_type,
                    'palsy': source_palsy,
                    'control': source_control
                })
                temp_nodes.append({
                    'id': target,
                    'nodeType': target_type,
                    'palsy': target_palsy,
                    'control': target_control
                })
                links.append(link)
            for item in temp_nodes:
                if item['id'] not in nodes_id:
                    nodes_id.append(item['id'])
                    nodes.append(item)
                else:
                    index = nodes_id.index(item['id'])
                    del nodes[index]
                    del nodes_id[index]
                    nodes.append(item)
                    nodes_id.append(item['id'])

            tmp_links = []
            # 去重
            for link in links:
                key = {
                    'source': link['source'],
                    'target': link['target'],
                    'flow': 0,
                    'times': 0,
                }
                if key not in tmp_links:
                    tmp_links.append(key)

            for item in tmp_links:
                for link in links:
                    if link['source'] == item['source'] and link['target'] == item['target']:
                        item['flow'] = item['flow'] + link['flow']
                        item['times'] = item['times'] + 1
            links = tmp_links

            end = time.clock()
            diff_time = end - start
            print("spend time for build graph: " + str(diff_time))

            # 计算flow
            for node in nodes:
                flow_in = 0
                flow_out = 0
                for link in links:
                    if node['id'] == link['source']:
                        flow_out = flow_out + link['flow']
                    if node['id'] == link['target']:
                        flow_in = flow_in + link['flow']
                node['flow_in'] = flow_in
                node['flow_out'] = flow_out
                node['flow'] = flow_in + flow_out
            result = {'nodes': nodes, 'links': links}
            start = time.clock()
            result = igraphLayout.cal_back_layout_data(result, layoutType)
            end = time.clock()
            diff_time = end - start
            print("spend time for calculate layout: " + str(diff_time))
            self.write(result)
            LocalGraph.updatelocaldata(nodes, result['links'])
        else:
            result = {'nodes': [], 'links': []}
            self.write(result)

    def post(self):
        self.set_header('Access-Control-Allow-Origin',
                        '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods",
                        "PUT,POST,GET,DELETE,OPTIONS")
        print('post')
        params = self.get_argument('params')
        params = json.loads(params)
        layoutType = params['layout_type']
        data = params['layoutData']
        data = json.loads(data)
        start = time.clock()
        result = igraphLayout.cal_back_layout_data(data, layoutType)
        end = time.clock()
        diff_time = end - start
        print("spend time for calculate layout: " + str(diff_time))
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",result['nodes'][0])
        self.write(result)


class getDim2(tornado.web.RequestHandler):
    # 获取降维数据
    def get(self):
        self.set_header('Access-Control-Allow-Origin',
                        '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods",
                        "PUT,POST,GET,DELETE,OPTIONS")
        params = json.loads(self.get_argument('params'))
        # print(params)
        type = int(params['type'])
        # type = int(json.loads(self.get_argument('type')))
        nodesobj = LocalGraph.getdim2(type)
        evt_unpacked = {
            'nodes': nodesobj,
            # 'edges': list(LocalGraph.G.edges()),
            'outlier': LocalGraph.outlierrecord
        }
        evt = json.dumps(evt_unpacked)
        self.write(evt)


class changeOutlierType(tornado.web.RequestHandler):
    # 改变检测outlier的方法
    def get(self):
        self.set_header('Access-Control-Allow-Origin',
                        '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods",
                        "PUT,POST,GET,DELETE,OPTIONS")
        params = json.loads(self.get_argument('params'))
        type = int(params['type'])
        LocalGraph.outliertype = type
        evt_unpacked = {}
        evt = json.dumps(evt_unpacked)
        self.write(evt)


class getAttr(tornado.web.RequestHandler):
    # 获取指定节点的指定属性变化记录
    def get(self):
        self.set_header('Access-Control-Allow-Origin',
                        '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods",
                        "PUT,POST,GET,DELETE,OPTIONS")
        params = json.loads(self.get_argument('params'))
        nodes = json.loads(params['nodes'])
        tmpattr, nodesattr = LocalGraph.getAttr(nodes)
        evt_unpacked = {
            "attr": tmpattr,
            'nodes': nodesattr,
            "start": LocalGraph.rangestart,
            "end": LocalGraph.rangeend
        }
        evt = json.dumps(evt_unpacked)
        self.write(evt)


class choosenone(tornado.web.RequestHandler):
    # 获取指定节点的指定属性变化记录
    def get(self):
        self.set_header('Access-Control-Allow-Origin',
                        '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods",
                        "PUT,POST,GET,DELETE,OPTIONS")
        LocalGraph.choosenone()
        evt_unpacked = {}
        evt = json.dumps(evt_unpacked)
        self.write(evt)


class gettree(tornado.web.RequestHandler):
    # 获取指定节点的指定属性变化记录
    def get(self):
        self.set_header('Access-Control-Allow-Origin',
                        '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods",
                        "PUT,POST,GET,DELETE,OPTIONS")
        params = json.loads(self.get_argument('params'))
        nodes = params['nodes']
        evt_unpacked = LocalGraph.singlesel(nodes)
        evt = json.dumps(evt_unpacked)
        self.write(evt)


class getSPs(tornado.web.RequestHandler):
    # 获取指定节点的指定属性变化记录
    def get(self):
        self.set_header('Access-Control-Allow-Origin',
                        '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods",
                        "PUT,POST,GET,DELETE,OPTIONS")
        params = json.loads(self.get_argument('params'))
        nodes = params['nodes']
        evt_unpacked = LocalGraph.multisel(nodes)
        # print(evt_unpacked)
        evt = json.dumps(evt_unpacked)
        self.write(evt)


class getFlow(tornado.web.RequestHandler):
    # 获取指定节点的指定属性变化记录
    def get(self):
        self.set_header('Access-Control-Allow-Origin',
                        '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods",
                        "PUT,POST,GET,DELETE,OPTIONS")
        params = json.loads(self.get_argument('params'))
        nodes = json.loads(params['nodes'])
        evt_unpacked = LocalGraph.flowdist(nodes)
        # print(evt_unpacked)
        evt = json.dumps(evt_unpacked)
        self.write(evt)


class getData2(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Access-Control-Allow-Origin',
                        '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods",
                        "PUT,POST,GET,DELETE,OPTIONS")
        params = json.loads(self.get_argument('params'))
        print('params', params)
        timeRange = json.loads(params['data'])
        print('timeRange', timeRange)
        global nowSelectedData
        start = time.clock()
        nowSelectedData = NetworkData.getTimeRangeData(timeRange[0],
                                                       timeRange[1])
        end = time.clock()
        diff_time = end - start
        print("spend time for get timeline data: " + str(diff_time))
        evt_unpacked = {'message': 'timeRangeData', 'data': nowSelectedData}
        evt = json.dumps(evt_unpacked)
        self.write(evt)
        LocalGraph.rangestart = LocalGraph.linuxtimestamp(timeRange[0])
        LocalGraph.rangeend = LocalGraph.linuxtimestamp(timeRange[1])


class getAnomalyLayoutData(tornado.web.RequestHandler):
    # 读取异常数据并且计算布局
    def get(self):
        self.set_header('Access-Control-Allow-Origin',
                        '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods",
                        "PUT,POST,GET,DELETE,OPTIONS")
        links = []
        nodes = []
        temp_nodes = []
        nodes_id = []
        tmp_links = []

        data = NetworkData.getAnomalyData("event2")

        for row in data:
            source = row['trans_node_global_no']
            target = row['recv_node_golbal_no']
            flow = row['flow']
            # 空值处理
            if(source != None and target != None):
                link = {'source': source, 'target': target, 'flow':flow}

                links.append(link)
                
                if target not in nodes_id:
                        nodes_id.append(target)
                        nodes.append({'id': target,'flow':flow,'flow_in':flow,'flow_out':0})
                else:
                    index = nodes_id.index(target)
                    temp=nodes[index]
                    temp['flow_in']=temp['flow_in']+flow
                    temp['flow']=temp['flow']+temp['flow_in']
                    del nodes_id[index]
                    del nodes[index]
                    nodes_id.append(target)
                    nodes.append(temp)

                if source not in nodes_id:
                        nodes_id.append(source)
                        nodes.append({'id': source,'flow':flow,'flow_in':0,'flow_out':flow})
                else:
                    index = nodes_id.index(source)
                    temp=nodes[index]
                    temp['flow_out']=temp['flow_out']+flow
                    temp['flow']=temp['flow']+temp['flow_out']
                    del nodes_id[index]
                    del nodes[index]
                    nodes_id.append(source)
                    nodes.append(temp)
            else:
                if source == None:
                    # temp_nodes.append({'id': target})
                    if target not in nodes_id:
                        nodes_id.append(target)
                        nodes.append({'id': target,'flow':flow,'flow_in':flow,'flow_out':0})
                    else:
                        index = nodes_id.index(target)
                        temp=nodes[index]
                        temp['flow_in']=temp['flow_in']+flow
                        temp['flow']=temp['flow']+temp['flow_in']
                        del nodes_id[index]
                        del nodes[index]
                        nodes_id.append(target)
                        nodes.append(temp)

                if target == None:
                    if source not in nodes_id:
                        nodes_id.append(source)
                        nodes.append({'id': source,'flow':flow,'flow_in':0,'flow_out':flow})
                    else:
                        index = nodes_id.index(source)
                        temp=nodes[index]
                        temp['flow_out']=temp['flow_out']+flow
                        temp['flow']=temp['flow']+temp['flow_out']
                        del nodes_id[index]
                        del nodes[index]
                        nodes_id.append(source)
                        nodes.append(temp)



        # 边处理
        for link in links:
            key = {
                'source': link['source'],
                'target': link['target'],
                'flow': 0,
                'times': 0,
            }
            if key not in tmp_links:
                tmp_links.append(key)
        for item in tmp_links:
            for link in links:
                if link['source'] == item['source'] and link['target'] == item['target']:
                    item['flow'] = item['flow']+link['flow']
                    item['times'] = item['times'] + 1
        links = tmp_links
        global AnomalyLayoutDataResult
        AnomalyLayoutDataResult = {'nodes': nodes, 'links': links}
        AnomalyLayoutDataResult = igraphLayout.cal_back_layout_data(
            AnomalyLayoutDataResult, 'kk')
        evt = json.dumps(AnomalyLayoutDataResult)
        self.write(evt)


class detectAnomalyOnFlow(tornado.web.RequestHandler):
    # 异常检测代码
    def get(self):
        self.set_header('Access-Control-Allow-Origin',
                        '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods",
                        "PUT,POST,GET,DELETE,OPTIONS")

        print('异常检测代码')
        nodes=[]
        links=[]
        AnomalyNodes=[]
        global AnomalyLayoutDataResult # 由于前端传输局过来经常失败所以这里采用了全局变量

        nodes=AnomalyLayoutDataResult['nodes'];
        links=AnomalyLayoutDataResult['links'];
        
        for node in nodes:
            sumFlow=node['flow']
            flow_out=0
            flow_in=0
            for link in links:
                if link['source']==node['id']:
                    flow_out=flow_out+link['flow']
                if link['target']==node['id']:
                    flow_in=flow_in+link['flow']
            if (flow_in+flow_out) !=sumFlow:
                AnomalyNodes.append({'id':node['id'],'flow_difference':sumFlow-(flow_in+flow_out),'node':node})

        evt = json.dumps(AnomalyNodes)
        self.write(evt)
    pass


class getTimeLineJson(tornado.web.RequestHandler):
    # 从预先计算好的json文件中，获取timeline全局流量
    def get(self):
        self.set_header('Access-Control-Allow-Origin',
                        '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods",
                        "PUT,POST,GET,DELETE,OPTIONS")
        params = json.loads(self.get_argument('params'))
        print('params', params)
        filePath = '../data/timeLineData_all.json'
        with codecs.open(filePath, 'r', 'utf-8') as load_f:
            load_dict = json.load(load_f)
        evt = json.dumps(load_dict)
        self.write(evt)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    print(
        'server running at 127.0.0.1:%d ...' % (tornado.options.options.port))
    print(client_file_root_path)
    app = tornado.web.Application(
        handlers=[
            (r'/recent-data', getRecentDataHandler),
            (r'/get-layout-data', getLayoutData),
            (r'/getDim2', getDim2),
            (r'/changeOutlierType', changeOutlierType),
            (r'/getAttr', getAttr),
            (r'/choosenone', choosenone),
            (r'/gettree', gettree),
            (r'/getSPs', getSPs),
            (r'/getFlow', getFlow),
            (r'/getData2', getData2),
            (r'/get-timeLine-json', getTimeLineJson),
            (r'/detect-anomaly-onflow', detectAnomalyOnFlow),
            (r'/get-anomaly-layout-data', getAnomalyLayoutData),
            (r'/(.*)', tornado.web.StaticFileHandler, {
                'path': client_file_root_path,
                'default_filename': 'index.html'
            })  # fetch client files
        ],
        debug=True,
    )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
