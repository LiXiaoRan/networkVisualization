# -*- coding: utf-8 -*-
# @Author: wakouboy
# @Date:   2018-08-12 20:16:26
# @Last Modified by:   wakouboy
# @Last Modified time: 2018-11-28 12:50:00
import pymysql
import time
import json
import time
from datetime import datetime, timedelta
#connect to the db
conn = pymysql.connect(host='192.168.10.9', db='transit_network', user = 'transitnet', password = 'pkuvistransit')
# conn = pymysql.connect(host='127.0.0.1', db='transit_network', user = 'root', password = '123456')

tablename = 'transitnet0515s'
cursor = conn.cursor()
class NetworkData:
    def __init__ (self):
        self.maxTime = 0

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
    def getDataByRecentTime(self, params):
        if self.maxTime == 0:
            sql = "select max(end_time) from " + tablename
            cursor.execute(sql)
            data = cursor.fetchall()
            self.maxTime = data[0][0]
            print(self.maxTime)

        end = timeConvert(self.maxTime)
        start = 0
        if params['timeRange'] == '1day':
            start = (end + timedelta(-1)).strftime('%Y%m%d%H%M%S') + self.maxTime[14:]
        end = self.maxTime
        print(start, end)
        key = 'end_time'
        sql = "select * from " + tablename + " where " + key + ">=" + "%s" + " and " + key + "<=" + "%s" + " limit " + "%s"
        cursor.execute(sql, [start, end, 5000])
        data = cursor.fetchall()

        sql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = %s"
        cursor.execute(sql, tablename)
        fields = cursor.fetchall()
        
        return {'data': data, 'fields': fields}

    def addGraph(self, data, name, tags, dt):
        sql = "insert into publicGraph(name, tags, data, time) values (%s, %s, %s, %s)"
        print(name, tags, dt)
        cursor.execute(sql, (name, tags, data, dt))
        conn.commit()
        return 1

def timeConvert(tstr):
    tstr = tstr[0:14]
    y = datetime.strptime(tstr, '%Y%m%d%H%M%S')
    return y
    

