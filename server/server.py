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

# import frq_path_stat
define("port", default=22333, type=int, help="run on the given port")

# client_file_root_path = os.path.join(os.path.split(__file__)[0],'../client')
client_file_root_path = os.path.join(os.path.split(__file__)[0], '../')
client_file_root_path = os.path.abspath(client_file_root_path)

NetworkData = database.NetworkData()
LocalGraph = graphfunc.LocalGraph()

typeArray = ["主机", "交换机", "服务器"]
attrtArray = ["置瘫", "控制", "正常"]


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


class calLayout(tornado.web.RequestHandler):

    def get(self):

        self.set_header('Access-Control-Allow-Origin', '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS")
        params = self.get_argument('params')
        params = json.loads(params)
        layoutType = params['layout_type']
        data = NetworkData.getData(params)
        links = []
        temp_nodes = []
        nodes = []
        start = time.clock()
        for row in data:
            source = row['send_node_global_id'].strip()
            target = row['receive_node_global_id'].strip()
            flow = row['val']
            link = {'source': source, 'target': target, 'flow': flow}
            temp_nodes.append(source)
            temp_nodes.append(target)
            links.append(link)
        temp_nodes = set(temp_nodes)
        for item in temp_nodes:
            type_int = random.randint(0, 2)
            attribute_int = random.randint(0, 2)
            node = {'id': item, 'nodeType': typeArray[type_int], 'nodeAttribute': attrtArray[attribute_int]}
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

        result = {'nodes': nodes, 'links': links}
        start = time.clock()
        result = igraphLayout.cal_back_layout_data(result, layoutType)
        end = time.clock()
        diff_time = end - start
        print("spend time for calculate layout: " + str(diff_time))
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", result['nodes'][0])
        self.write(result)
        LocalGraph.updatelocaldata(result['links'], 0)

    def post(self):
        self.set_header('Access-Control-Allow-Origin', '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS")
        constraint = self.get_argument('constraint')
        constraint = json.loads(constraint)
        self.write({'suc': 'post success'})


class getLayoutData(tornado.web.RequestHandler):
    '''计算前端选择布局后提交的数据'''

    def get(self):
        print("进入get")
        self.set_header('Access-Control-Allow-Origin', '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS")
        params = self.get_argument('params')
        params = json.loads(params)
        layoutType = params['layout_type']
        data = params['layoutData']
        # print("data in getLayoutData is ")
        # print(data)
        start = time.clock()
        result = igraphTest.cal_back_layout_data(data, layoutType)
        end = time.clock()
        diff_time = end - start
        print("spend time for calculate layout: " + str(diff_time))
        self.write(result)

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
        result = igraphTest.cal_back_layout_data(data, layoutType)['result']
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
        nodes_new, results_new = LocalGraph.getdim2(type)
        evt_unpacked = {'nodes': nodes_new, 'nodes_embedded': results_new.tolist(), 'edges': list(LocalGraph.G.edges()),
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
        type = int(params['type'])
        nodes = json.loads(params['nodes'])
        # print(type,nodes)
        tmpattr = LocalGraph.getAttr(type, nodes)
        evt_unpacked = {"attr": tmpattr}
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


class getBFStree(tornado.web.RequestHandler):
    # 获取指定节点的指定属性变化记录
    def get(self):
        self.set_header('Access-Control-Allow-Origin', '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS")
        params = json.loads(self.get_argument('params'))
        nodes = params['nodes']
        # nodes=[list(LocalGraph.G.nodes())[0]]
        evt_unpacked = LocalGraph.getBFStree(nodes)
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
        # nodes = [list(LocalGraph.G.nodes())[0],list(LocalGraph.G.nodes())[1]]
        evt_unpacked = LocalGraph.getSPs(nodes)
        # print(evt_unpacked)
        evt = json.dumps(evt_unpacked)
        self.write(evt)


class getSubgraph(tornado.web.RequestHandler):
    # 获取指定节点的指定属性变化记录
    def get(self):
        self.set_header('Access-Control-Allow-Origin', '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS")
        params = json.loads(self.get_argument('params'))
        nodes = params['nodes']
        # nodes = [list(LocalGraph.G.nodes())[0], list(LocalGraph.G.nodes())[1], list(LocalGraph.G.nodes())[2]]
        evt_unpacked = LocalGraph.getSubgraph(nodes)
        # print(evt_unpacked)
        evt = json.dumps(evt_unpacked)
        self.write(evt)


class getsubdata(tornado.web.RequestHandler):
    # 获取指定节点的指定属性变化记录
    def get(self):
        self.set_header('Access-Control-Allow-Origin', '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS")
        evt_unpacked = LocalGraph.getsubdata()
        evt = json.dumps(evt_unpacked)
        self.write(evt)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    print('server running at 127.0.0.1:%d ...' % (tornado.options.options.port))
    print(client_file_root_path)
    app = tornado.web.Application(
        handlers=[
            (r'/recent-data', getRecentDataHandler),
            (r'/cal-layout', calLayout),
            (r'/get-layout-data', getLayoutData),
            (r'/getDim2', getDim2),
            (r'/changeOutlierType', changeOutlierType),
            (r'/getAttr', getAttr),
            (r'/choosenone', choosenone),
            (r'/getBFStree', getBFStree),
            (r'/getSPs', getSPs),
            (r'/getSubgraph', getSubgraph),
            (r'/getsubdata', getsubdata),
            (r'/(.*)', tornado.web.StaticFileHandler, {'path': client_file_root_path,
                                                       'default_filename': 'index.html'})  # fetch client files
        ],
        debug=True,
    )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
