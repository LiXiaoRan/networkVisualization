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
import igraphTest

# import frq_path_stat
define("port", default=22333, type=int, help = "run on the given port")

# client_file_root_path = os.path.join(os.path.split(__file__)[0],'../client')
client_file_root_path = os.path.join(os.path.split(__file__)[0],'../')
client_file_root_path = os.path.abspath(client_file_root_path)

NetworkData = database.NetworkData()


 
class getRecentDataHandler(tornado.web.RequestHandler):
    def post(self):
      self.set_header('Access-Control-Allow-Origin','*')  # 添加响应头，允许指定域名的跨域请求
      self.set_header("Access-Control-Allow-Headers", "X-Requested-With");  
      self.set_header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS"); 


    def get(self):
      # 时间轴获取统计数据
      self.set_header('Access-Control-Allow-Origin','*')  # 添加响应头，允许指定域名的跨域请求
      self.set_header("Access-Control-Allow-Headers", "X-Requested-With");  
      self.set_header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS"); 
      params = self.get_argument('params')
      params = json.loads(params)
      data = NetworkData.getDataByRecentTime(params)
      self.write(data)



class calLayout(tornado.web.RequestHandler):

    def get(self):

        self.set_header('Access-Control-Allow-Origin','*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With");  
        self.set_header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS"); 
        params = self.get_argument('params')
        params = json.loads(params)
        # print(layoutType)
        print(params)
        layoutType=params['layout_type']
        data = NetworkData.getData(params)['data']
        links=[]
        temp_nodes=[]
        nodes=[]
        for row in data:
            source=row[4]
            target=row[6]
            edge={'source':source,'target':target}
            temp_nodes.append(source)
            temp_nodes.append(target)
            links.append(edge)
        temp_nodes=set(temp_nodes)

        print('node number', len(temp_nodes))
        for item in temp_nodes:
            node={'id':item}
            nodes.append(node)

        result={'nodes':nodes,'links':links}
        start=time.clock()
        result=igraphTest.cal_back_layout_data(result,layoutType)
        end=time.clock()
        diff_time=end-start
        print("spend time for calculate layout: "+str(diff_time))

        self.write(result)


    def post(self):
        self.set_header('Access-Control-Allow-Origin','*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With");  
        self.set_header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS"); 
        constraint=self.get_argument('constraint')
        constraint = json.loads(constraint)
        self.write({'suc':'post success'})


class getLayoutData(tornado.web.RequestHandler):
    '''计算前端选择布局后提交的数据'''
    def get(self):
        print("进入get")
        self.set_header('Access-Control-Allow-Origin','*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With");  
        self.set_header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS");
        params = self.get_argument('params')
        params = json.loads(params)
        layoutType=params['layout_type']
        data=params['layoutData']
        # print("data in getLayoutData is ")
        # print(data)
        start=time.clock()
        result=igraphTest.cal_back_layout_data(data,layoutType)
        end=time.clock()
        diff_time=end-start
        print("spend time for calculate layout: "+str(diff_time))
        self.write(result)

    def post(self):
        self.set_header('Access-Control-Allow-Origin','*')  # 添加响应头，允许指定域名的跨域请求
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With");  
        self.set_header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS"); 
        print('post')
        params = self.get_argument('params')
        params = json.loads(params)
        layoutType=params['layout_type']
        data=params['layoutData']
        data = json.loads(data)
        start=time.clock()
        result=igraphTest.cal_back_layout_data(data,layoutType)
        end=time.clock()
        diff_time=end-start
        print("spend time for calculate layout: "+str(diff_time))
        self.write(result)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    print('server running at 127.0.0.1:%d ...'%(tornado.options.options.port))
    print(client_file_root_path)
    app = tornado.web.Application(
        handlers=[
                  (r'/recent-data', getRecentDataHandler), 
                  (r'/cal-layout', calLayout),
                  (r'/get-layout-data', getLayoutData),
                  # (r'/checkClassName', checkClassNameHandler),
                  # (r'/queryCarList', queryCarListHandler),
                  (r'/(.*)', tornado.web.StaticFileHandler, {'path': client_file_root_path,
                                               'default_filename': 'index.html'}) # fetch client files
                  ],
        debug=True,
    )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
