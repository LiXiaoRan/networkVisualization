# -*- coding: utf-8 -*-
# @Author: wakouboy
# @Date:   2018-08-12 20:16:26
# @Last Modified by:   wakouboy
# @Last Modified time: 2018-11-30 16:40:38
import pymysql
import time
import json
import time
from datetime import datetime, timedelta
#connect to the db
conn = pymysql.connect(host='192.168.10.9', db='transit_network', user = 'transitnet', password = 'pkuvistransit', cursorclass=pymysql.cursors.DictCursor)
# conn = pymysql.connect(host='127.0.0.1', db='transit_network', user = 'root', password = '123456', cursorclass=pymysql.cursors.DictCursor)

tablename = 'transitnet0515s'

class NetworkData:
    def __init__ (self):
        self.maxTime = 0

    def getData(self, params):
        key = list(params['where'].keys())[0]
        start = params['where'][key]['start']
        end = params['where'][key]['end']
        sql = "select * from " + tablename + " where " + key + ">=" + "%s" + " and " + key + "<=" + "%s" + " limit " + "%s"
        start=time.clock()
        data = []
        with conn.cursor() as cursor:
            cursor.execute(sql, [start, end, params['limit']])
            data = cursor.fetchall()
        end=time.clock()
        diff_time=end-start
        print("spend time for search database: "+str(diff_time))
        return data
    def getDataByRecentTime(self, params):
        if self.maxTime == 0:
            with conn.cursor() as cursor:
                sql = "select max(end_time) from " + tablename
                cursor.execute(sql)
                data = cursor.fetchall()
                self.maxTime = data[0]['max(end_time)']
                print(self.maxTime)

        end = timeConvert(self.maxTime)
        start = 0
        if params['timeRange'] == '1day':
            start = (end + timedelta(-1)).strftime('%Y%m%d%H%M%S') + self.maxTime[14:]
        end = self.maxTime
        print(start, end)
        key = 'end_time'
        sql = "select * from " + tablename + " where " + key + ">=" + "%s" + " and " + key + "<=" + "%s"
        with conn.cursor() as cursor:
            cursor.execute(sql, [start, end])
            data = cursor.fetchall()
            return data

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
    

