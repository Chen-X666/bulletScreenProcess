# _*_ coding: utf-8 _*_
"""
Time:     2021/8/7 20:58
Author:   ChenXin
Version:  V 0.1
File:     MysqlDatabase.py
Describe:  Github link: https://github.com/Chen-X666
"""
import pymysql
def databaseSetting():
    db = pymysql.Connect(
            host='cdb-2m6kkrcx.gz.tencentcdb.com',  # 服务器地址
            port=10165,  # 服务器端口号
            user='root',  # 用户名
            passwd='972113786@qq.com',  # 密码
            db='bilibili_bullet',  # 数据库名
            charset='utf8'  # 编码式
        )
    return db
