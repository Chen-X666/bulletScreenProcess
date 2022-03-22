# _*_ coding: utf-8 _*_
"""
Time:     2021/8/7 13:38
Author:   ChenXin
Version:  V 0.1
File:     BulletDataFliter.py
Describe:  Github link: https://github.com/Chen-X666
"""
from random import random

import pymysql
import getDataBySql.MysqlDatabase as dbSetting
import pandas as pd
import numpy as np

from DatabaseUtil.DBUtil import DbPoolUtil


def connectDatabase(sql):
    db = dbSetting.databaseSetting()
    cursor = db.cursor()
    cursor.execute(sql)
    col_result = cursor.description
    results = cursor.fetchall()
    db.close()
    print('*********数据第一行**********')
    try:
        print(results[0])
    except:
        print('None')

    return col_result,results

def getVideoBvno():
    sql = "SELECT videoBvno FROM `video_table`"
    return connectDatabase(sql)

def getBulletDataByDate(videoType, startData, endData):
    sql = "SELECT * " \
          "FROM %s_bullet_table " \
          "WHERE sendTime>= %d " \
          "AND sendTime <= %d"%(videoType,startData,endData)
    print(sql)
    return connectDatabase(sql)

def getBulletDataByBv(videoType,videoBvno):
    sql = "SELECT bulletContent " \
          "FROM %s_bullet_table" \
          " WHERE videoBvno = '%s' "%(videoType,videoBvno)
    print(sql)
    return connectDatabase(sql)

def getBulletDataByBvUnionVideoTime(videoType,videoBvno):
    sql = "SELECT * " \
          "FROM(SELECT * " \
          "FROM %s_bullet_table " \
          "WHERE videoBvno = '%s') as a " \
          "JOIN video_table as b on a.videoBvno = b.videoBvno"%(videoType,videoBvno)
    print(sql)
    return connectDatabase(sql)

def getcsv(rel,columns,csv_path):
    data1 = list(map(list, rel))
    df = pd.DataFrame(data=data1,columns=columns)  # mysql查询的结果为元组，需要转换为列表
    df.to_csv(csv_path,index=False)

if __name__ == '__main__':
    db_pool_util = DbPoolUtil(db_type="mysql")
    sql = "SELECT * " \
          "FROM(SELECT * " \
          "FROM %s_bullet_table " \
          "WHERE videoBvno = '%s') as a " \
          "JOIN video_table as b on a.videoBvno = b.videoBvno"%(videoType,videoBvno)
    db_pool_util.execute_query(sql)
    # 获取字段名，以列表形式保存
    # columns = []
    # col_result,results = getBulletDataByDate(videoType='yiqing', startData=1579536000, endData=1581955200)
    # for i in range(0, len(col_result)):
    #     columns.append(col_result[i][0])
    # getcsv(rel=results,columns=columns,csv_path='data/疫情爆发期1.csv')
    print(0/0)


