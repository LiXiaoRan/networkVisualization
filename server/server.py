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

# import frq_path_stat
define("port", default=22333, type=int, help="run on the given port")

# client_file_root_path = os.path.join(os.path.split(__file__)[0],'../client')
client_file_root_path = os.path.join(os.path.split(__file__)[0], '../')
client_file_root_path = os.path.abspath(client_file_root_path)

NetworkData = database.NetworkData()
LocalGraph = graphfunc.LocalGraph()

typeArray = ["主机", "交换机", "服务器"]
attrtArray = ["致瘫", "控制", "正常"]


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
            source = row['trans_node_global_no'].strip()
            target = row['recv_node_golbal_no'].strip()
            flow = row['flow']
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
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", result['nodes'][0])
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
        result = igraphLayout.cal_back_layout_data(data, layoutType)
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


class getData(tornado.web.RequestHandler):
    #获取timeline指定时间段的数据
    def get(self):
        self.set_header('Access-Control-Allow-Origin', '*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS")
        params = json.loads(self.get_argument('params'))
        print('params', params)
        timeRange = json.loads(params['data'])
        print('timeRange', timeRange[0], timeRange[1])
        start = time.clock()
        data = NetworkData.getTimeRangeData(timeRange[0], timeRange[1])
        end = time.clock()
        diff_time = end - start
        print("spend time for get timeLine data: " + str(diff_time))
        newdata=[]
        i=0
        while i<len(data)-1:
            sttime=data[i]["start_time"]
            sttime=sttime[0:14]
            sttime2 = data[i+1]["start_time"]
            sttime2 = sttime2[0:14]
            sttimeStamp = int(time.mktime(time.strptime(sttime, "%Y%m%d%H%M%S")))
            sttimeStamp2 = int(time.mktime(time.strptime(sttime2, "%Y%m%d%H%M%S")))

            sttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(sttimeStamp))
            sttime2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(sttimeStamp2))

            value1=int(float(data[i]["val"]))
            value2 = int(float(data[i+1]["val"]))

            if((sttimeStamp2-sttimeStamp)>1000):
                buckets=int((sttimeStamp2-sttimeStamp))
                for j in xrange(0,buckets,10):
                    timeArray = time.localtime(sttimeStamp+(j+1))
                    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                    newdata.append({otherStyleTime:0})
            elif (sttimeStamp2-sttimeStamp !=0):
                newdata.append({sttime:math.sqrt(value1)})
            elif (sttimeStamp2-sttimeStamp ==0):
                if len(newdata):newdata.pop()
                newdata.append({sttime: math.sqrt(value1+value2)})
                i=i+1
            i=i+1

        timerange0=timeRange[0][0:14]
        timerange0S=int(time.mktime(time.strptime(timerange0, "%Y%m%d%H%M%S")))
        timerange0 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timerange0S))
        timerange1 = timeRange[1][0:14]
        timerange1S = int(time.mktime(time.strptime(timerange1, "%Y%m%d%H%M%S")))
        timerange1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timerange1S))

        mintime = data[0]["start_time"][0:14]
        mintimeS = int(time.mktime(time.strptime(mintime, "%Y%m%d%H%M%S")))
        maxtime = data[(len(data)-1)]["start_time"][0:14]
        maxtimeS = int(time.mktime(time.strptime(maxtime, "%Y%m%d%H%M%S")))

        print(mintime,maxtime)
        if (mintimeS-timerange0S)>300:
            newdata.insert(0, {timerange0:0})
            newdata.insert(1, {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mintimeS-1)): 0})
        if (timerange1S-maxtimeS)>300:
            newdata.append({time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(maxtimeS+1)): 0})
            newdata.append({timerange1: 0})

        #print newdata
        #evt_unpacked = {'message': 'timeRangeData', 'data': data }
        evt_unpacked = {'message': 'timeRangeData', 'data': newdata, 'timeLineData': data }
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
        data = NetworkData.getTimeRangeData(timeRange[0], timeRange[1])
        print(len(data))
        evt_unpacked = {'message': 'timeRangeData', 'data': data }
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
            (r'/getData', getData),
            (r'/getData2', getData2),
            (r'/(.*)', tornado.web.StaticFileHandler, {'path': client_file_root_path,
                                                       'default_filename': 'index.html'})  # fetch client files
        ],
        debug=True,
    )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
