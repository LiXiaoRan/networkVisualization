# -*- coding: utf-8 -*-
# @Author: wakouboy
# @Date:   2018-08-12 20:16:26
# @Last Modified by:   wakouboy
# @Last Modified time: 2018-11-05 17:33:41
import pymysql
import time
import json
import time
#connect to the db
conn = pymysql.connect(host='192.168.10.9', db='transit_network', user = 'transitnet', password = 'pkuvistransit')
tablename = 'transitnet0515s'
cursor = conn.cursor()
class NetworkData:
    def __init__ (self):
        self.authorHouse = {}
        self.authorDict = {}

    def getData(self, params):
        key = list(params['where'].keys())[0]
        start = params['where'][key]['start']
        end = params['where'][key]['end']
        sql = "select * from " + tablename + " where " + key + ">=" + "%s" + " and " + key + "<=" + "%s" + " limit " + "%s"
        print(sql)
        start=time.clock()
        cursor.execute(sql, [start, end, params['limit']])
        data = cursor.fetchall()
        end=time.clock()
        diff_time=end-start
        print("spend time for search database: "+str(diff_time))
        sql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = %s"
        cursor.execute(sql, tablename)
        fields = cursor.fetchall()
        return {'data': data, 'fields': fields}
    def getPublicGraphInfo(self):
        # sql = "select * from authorDict where name = %s"
        sql = "select id, name, tags, time from publicGraph"
        data = ''
        try:
            cursor.execute(sql)
            data = cursor.fetchall()
        except Exception as e:
            print(e)
        # print(data)
        return data
    def getPublicGraphData(self, graphId):
        # sql = "select * from authorDict where name = %s"
        sql = "select data from publicGraph where id = %s"
        cursor.execute(sql, graphId)

        data = cursor.fetchall()
        print(data)
        return data
    def addGraph(self, data, name, tags, dt):
        sql = "insert into publicGraph(name, tags, data, time) values (%s, %s, %s, %s)"
        print(name, tags, dt)
        cursor.execute(sql, (name, tags, data, dt))
        conn.commit()
        return 1
