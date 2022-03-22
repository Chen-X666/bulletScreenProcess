# _*_ coding: utf-8 _*_
"""
Time:     2021/11/15 20:14
Author:   ChenXin
Version:  V 0.1
File:     Bullet.py
Describe:  Github link: https://github.com/Chen-X666
"""
import asyncio
import time

import random

from aiohttp import ServerDisconnectedError
from bilibili_api import video, Credential
import datetime
import pandas as pd
from bilibili_api.exceptions import NetworkException


async def getVideoMsg(bvid):
    # 实例化 Video 类
    v = video.Video(bvid=bvid)
    # 获取信息
    info = await v.get_info()
    # 打印信息
    print(info)
    return info


async def getBullets(credential,bvid,bulletDate=None):
    # 实例化 Video 类
    v = video.Video(bvid=bvid,credential=credential)
    #根据BVid与日期获取弹幕
    try:
        info = await v.get_danmakus(page_index=0,date=bulletDate)
    except (ServerDisconnectedError,NetworkException):
        info = await v.get_danmakus(page_index=0, date=bulletDate)
        open('error.txt','a+').write('1')
    bullets = []
    for dm in info:
        bullet = []
        bullet.append(bvid)
        bullet.append(dm.crc32_id)
        bullet.append(dm.send_time)
        bullet.append(dm.text)
        bullet.append(dm.dm_time)
        #bullet.append(dm.text)
        bullet.append(dm.color)
        #bullet.append(dm.mode)
        bullet.append(dm.font_size)
        #bullet.append(dm.crc32_id)
        #bullet.append(dm.is_sub)
        bullet.append(dm.weight)
        bullet.append(dm.id)
        bullet.append(dm.id_str)
        bullet.append(dm.action)
        bullet.append(dm.mode)
        bullet.append(dm.is_sub)
        bullet.append(dm.pool)
        bullet.append(dm.attr)
        bullets.append(bullet)
    print(bullets)
    return bullets
#bvno,sendUserCrc32id,sendTime,text,sendVideoTime,color,fontSize,weight,id,idStr,action,mode,isSub,pool,attr
#获取队头时间
def getBulletHeadDate(bullets):
    DataList = []
    for i in bullets:
        DataList.append(i[2])
        # bulletDate = time.localtime(int(i[0]))
    #print(time.strftime("%Y-%m-%d", time.localtime(min(DataList))))
    return datetime.datetime.date(datetime.datetime.strptime(time.strftime("%Y-%m-%d", time.localtime(min(DataList))),'%Y-%m-%d'))


def saveBullets(bvid,bullets):

    # title
    name = ['bvno','dm_sendTime', 'dm_time', 'dm_text', 'dm_color', 'dm_mode', 'dm_fontSize',
            'dm_userId','dm_isSub','dm_weight','id','id_str','action','pool','attr']
    # bulletCollection
    data = pd.DataFrame(columns=name, data=bullets)
    # print(data)
    print(len(data))
    # delete duplicates
    data = data.drop_duplicates()
    print(len(data))
    data.to_csv('bullet_table_test.csv', encoding='utf-8', index=False,mode="a+")

def getCredential(i):
    credentials = []
    credential1 = Credential(sessdata='2537e31f%2C1661156988%2C3329f*21',
                            bili_jct='0ad58f3977dab3b0ad8a492d360c4d25',
                            buvid3='9F4A49E1-B555-4DE8-806F-8511ADFA72F8148811infoc')
    credential2 = Credential(sessdata='c10ed0f9%2C1660276898%2Cfe2b5*21',
                            bili_jct='94aeb8e8ca81659b65c69521de27c90c',
                            buvid3='0D4ED775-4148-79FC-805B-5E0F7B1472FB68155infoc')
    credential3 = Credential(sessdata='3850da70%2C1651735927%2C472a7*b1',
                            bili_jct='226be5c410c8c03b99376041c70375cb',
                            buvid3='A6579632-E92C-D856-18B9-5807561038C001195infoc')
    credentials.append(credential1)
    credentials.append(credential2)
    credentials.append(credential3)
    print('正在使用')
    print(i%3)
    return credentials[i%1]

if __name__ == '__main__':
    # 实例化 Credential 类
    # 这里是你的cookies
    bvids = ['BV127411v7pm','BV1SJ411V7Mb']
    #bvids = pd.read_csv('../videoCollection/data/Wvideo_table.csv',encoding='utf-8')['bvno'].to_list()
    creId = 0
    for bvid in bvids:
        # credential = Credential(sessdata='5dabb3ba%2C1648511023%2C0302f%2A91',
        #                         bili_jct='d06ec61ab04ae8968ccf6d7ffb261610',
        #                         buvid3='9F4A49E1-B555-4DE8-806F-8511ADFA72F8148811infoc')
        #credential = getCredential(creId)
        #获取视频发布时间
        pubdate = asyncio.get_event_loop().run_until_complete(getVideoMsg(bvid=bvid))["pubdate"]
        pubdate = time.strftime("%Y-%m-%d", time.localtime(pubdate))
        #定义爬取弹幕的时间
        #bulletDate = datetime.date(2020, 7, 27)
        #定义爬取时间等于今天
        bulletDate = datetime.date.today()
        print(bulletDate)
        #爬取弹幕
        bullets = asyncio.get_event_loop().run_until_complete(getBullets(credential=getCredential(creId),bvid=bvid,bulletDate=bulletDate))
        #如果爬取时间是上传时间
        while str(bulletDate) != str(pubdate):
            bulletHeadDate = getBulletHeadDate(bullets=bullets)
            print('弹幕队头日期为{date}'.format(date=bulletHeadDate))
            print('{date}爬取完毕'.format(date=bulletDate))
            print(bulletHeadDate)
            if  bulletHeadDate>=bulletDate:
                #如果队头时间大于等于爬取时间则爬取时间-1天
                bulletDate = bulletDate - datetime.timedelta(days=1)
                print('正在爬取弹幕日期{date}'.format(date=bulletDate))
                time.sleep(1)
                creId =creId+1
                bulletTemp = asyncio.get_event_loop().run_until_complete(
                    getBullets(credential=getCredential(creId), bvid=bvid, bulletDate=bulletDate))
                if len(bulletTemp)==0: break
                for i in bulletTemp:
                    bullets.append(i)
            else:
                #否则等于队头时间
                bulletDate = bulletHeadDate
                print('正在爬取弹幕日期{date}'.format(date=bulletDate))
                time.sleep(2)
                creId = creId + 1
                for i in asyncio.get_event_loop().run_until_complete(
                    getBullets(credential=getCredential(creId), bvid=bvid, bulletDate=bulletDate)):
                    bullets.append(i)
        #再爬一次发布日期
        creId = creId + 1
        print('爬发布日期')
        for i in asyncio.get_event_loop().run_until_complete(
                getBullets(credential=getCredential(creId), bvid=bvid,bulletDate=datetime.datetime.strptime(pubdate,"%Y-%m-%d"))):
            bullets.append(i)
        saveBullets(bullets=bullets,bvid=bvid)
        print('{bvid}爬取结束'.format(bvid=bvid))