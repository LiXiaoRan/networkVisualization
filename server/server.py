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
        self.set_header('Access-Control-Allow-Origin', '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS")

    def get(self):
        # 时间轴获取统计数据
        self.set_header('Access-Control-Allow-Origin', '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS")
        params = self.get_argument('params')
        params = json.loads(params)
        data = NetworkData.getDataByRecentTime(params)
        self.write({'data': data})


class getLayoutData(tornado.web.RequestHandler):
    # 计算前端选择布局后提交的数据
    def get(self):
        print("进入get")
        self.set_header('Access-Control-Allow-Origin', '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS")
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
        links = []
        temp_nodes = []
        nodes = []
        start = time.clock()
        for row in data:
            source = row['trans_node_global_no'].strip()
            target = row['recv_node_golbal_no'].strip()
            flow = row['flow']
            link = {'source': source, 'target': target, 'flow': flow}
            temp_nodes.append(source)
            temp_nodes.append(target)
            links.append(link)
        temp_nodes = set(temp_nodes)
        for item in temp_nodes:
            # 0 主机, 1 交换机, 2 服务器
            type_int = random.randint(0, 2)
            control = random.randint(0, 4)
            palsy = random.randint(0, 4)
            node = {'id': item, 'nodeType': type_int, 'control': control, 'palsy': palsy}
            nodes.append(node)

        tmp_links = []
        # 去重
        for link in links:
            key = {'source': link['source'], 'target': link['target'], 'flow': 0}
            if key not in tmp_links:
                tmp_links.append(key)

        for item in tmp_links:
            for link in links:
                if link['source'] == item['source'] and link['target'] == item['target']:
                    item['flow'] = item['flow'] + link['flow']
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

    def post(self):
        self.set_header('Access-Control-Allow-Origin', '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS")
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
        self.set_header('Access-Control-Allow-Origin', '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS")
        params = json.loads(self.get_argument('params'))
        # print(params)
        type = int(params['type'])
        # type = int(json.loads(self.get_argument('type')))
        nodesobj = LocalGraph.getdim2(type)
        evt_unpacked = {'nodes': nodesobj,
                        # 'edges': list(LocalGraph.G.edges()),
                        'outlier': LocalGraph.outlierrecord}
        evt = json.dumps(evt_unpacked)
        self.write(evt)


class changeOutlierType(tornado.web.RequestHandler):
    # 改变检测outlier的方法
    def get(self):
        self.set_header('Access-Control-Allow-Origin', '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS")
        params = json.loads(self.get_argument('params'))
        type = int(params['type'])
        LocalGraph.outliertype = type
        evt_unpacked = {}
        evt = json.dumps(evt_unpacked)
        self.write(evt)


class getAttr(tornado.web.RequestHandler):
    # 获取指定节点的指定属性变化记录
    def get(self):
        self.set_header('Access-Control-Allow-Origin', '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS")
        params = json.loads(self.get_argument('params'))
        nodes = json.loads(params['nodes'])
        tmpattr, nodesattr = LocalGraph.getAttr(nodes)
        evt_unpacked = {"attr": tmpattr, 'nodes': nodesattr, "start": LocalGraph.rangestart, "end": LocalGraph.rangeend}
        evt = json.dumps(evt_unpacked)
        self.write(evt)


class choosenone(tornado.web.RequestHandler):
    # 获取指定节点的指定属性变化记录
    def get(self):
        self.set_header('Access-Control-Allow-Origin', '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS")
        LocalGraph.choosenone()
        evt_unpacked = {}
        evt = json.dumps(evt_unpacked)
        self.write(evt)


class gettree(tornado.web.RequestHandler):
    # 获取指定节点的指定属性变化记录
    def get(self):
        self.set_header('Access-Control-Allow-Origin', '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS")
        params = json.loads(self.get_argument('params'))
        nodes = params['nodes']
        evt_unpacked = LocalGraph.singlesel(nodes)
        evt = json.dumps(evt_unpacked)
        self.write(evt)


class getSPs(tornado.web.RequestHandler):
    # 获取指定节点的指定属性变化记录
    def get(self):
        self.set_header('Access-Control-Allow-Origin', '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS")
        params = json.loads(self.get_argument('params'))
        nodes = params['nodes']
        evt_unpacked = LocalGraph.multisel(nodes)
        # print(evt_unpacked)
        evt = json.dumps(evt_unpacked)
        self.write(evt)


class getData2(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Access-Control-Allow-Origin', '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS")
        params = json.loads(self.get_argument('params'))
        print('params', params)
        timeRange = json.loads(params['data'])
        print('timeRange', timeRange)
        global nowSelectedData
        nowSelectedData = NetworkData.getTimeRangeData(timeRange[0], timeRange[1])
        evt_unpacked = {'message': 'timeRangeData', 'data': nowSelectedData}
        evt = json.dumps(evt_unpacked)
        self.write(evt)
        LocalGraph.rangestart = timeRange[0]
        LocalGraph.rangeend = timeRange[1]


class getTimeLineJson(tornado.web.RequestHandler):
    # 从预先计算好的json文件中，获取timeline全局流量
    def get(self):
        self.set_header('Access-Control-Allow-Origin', '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS")
        params = json.loads(self.get_argument('params'))
        print('params', params)
        filePath = '../data/timeLineData_all.json'
        with codecs.open(filePath, 'r', 'utf-8') as load_f:
            load_dict = json.load(load_f)
        evt = json.dumps(load_dict)
        self.write(evt)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    print('server running at 127.0.0.1:%d ...' % (tornado.options.options.port))
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
            (r'/getData2', getData2),
            (r'/get-timeLine-json', getTimeLineJson),
            (r'/(.*)', tornado.web.StaticFileHandler, {'path': client_file_root_path,
                                                       'default_filename': 'index.html'})  # fetch client files
        ],
        debug=True,
    )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
