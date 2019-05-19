# -*- coding: utf-8 -*-
# @Author: wakouboy
# @Date:   2018-08-12 20:16:26
# @Last Modified by:   wakouboy
# @Last Modified time: 2019-02-14 13:14:44
import pymysql
import time
import json
import time
from datetime import datetime, timedelta

# connect to the db
# conn = pymysql.connect(host='192.168.10.9', db='transit_network', user = 'transitnet', password = 'pkuvistransit', cursorclass=pymysql.cursors.DictCursor)
# conn = pymysql.connect(host='127.0.0.1', db='transit_network', user='root', password='584007',
#                        cursorclass=pymysql.cursors.DictCursor)
# conn = pymysql.connect(
#     host='127.0.0.1',
#     db='transit_network',
#     user='root',
#     password='Corner',
#     cursorclass=pymysql.cursors.DictCursor)
conn = pymysql.connect(host='127.0.0.1', db='transit_network', user='root', password='123456',
                        cursorclass=pymysql.cursors.DictCursor)

tablename = 'EVENT'


class NetworkData:
    def __init__(self):
        self.maxTime = 0

    def getDataByRecentTime(self, params):
        if self.maxTime == 0:
            with conn.cursor() as cursor:
                sql = "select max(event_endtime) from " + tablename
                cursor.execute(sql)
                data = cursor.fetchall()
                self.maxTime = data[0]['max(event_endtime)']
                print(self.maxTime)

        end = timeConvert(self.maxTime)
        start = 0
        if params['timeRange'] == '1day':
            start = (end + timedelta(-0.1)
                     ).strftime('%Y%m%d%H%M%S') + self.maxTime[14:]
        end = self.maxTime
        print(start, end)
        key = 'event_endtime'
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

    def getTimeRangeData(self, begin, end):
        sql = "select * from " + tablename + " where event_begintime >= %s and event_endtime <= %s order by event_begintime"
        data = ''
        with conn.cursor() as cursor:
            cursor.execute(sql, [begin, end])
            data = cursor.fetchall()
        return data

    def getAnomalyData(self,tablename):
        # 获取异常数据库的数据
        featchSql="SELECT * FROM "+tablename;
        with conn.cursor() as cursor:
            cursor.execute(featchSql);
            data = cursor.fetchall();
        return data
        


def timeConvert(tstr):
    tstr = tstr[0:14]
    y = datetime.strptime(tstr, '%Y%m%d%H%M%S')
    return y
