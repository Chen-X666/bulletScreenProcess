# _*_ coding: utf-8 _*_
"""
Time:     2022/1/4 11:25
Author:   ChenXin
Version:  V 0.1
File:     get_video_msg.py
Describe:  Github link: https://github.com/Chen-X666
"""
import asyncio
import time
from bilibili_api import video, Credential
import datetime
import pandas as pd
from bilibili_api.exceptions import ResponseCodeException


async def getVideoMsg(bvid):
    # 实例化 Video 类
    v = video.Video(bvid=bvid)
    # 获取信息
    info = await v.get_info()

    print(info)
    return info

async def getVideoTag(bvid):
    # 实例化 Video 类
    v = video.Video(bvid=bvid)
    # 获取信息
    tags = await v.get_tags()
    result = '|'
    for i in tags:
        result = result + i['tag_name']+'|'
    return result

async def getVideoStat(bvid):
    # 实例化 Video 类
    v = video.Video(bvid=bvid)
    # 获取信息
    stat = await v.get_stat()
    return stat

def saveVideos(videoData):

    # title
    name = ['bvno', 'tname', 'tag_name', 'owner_mid', 'owner_name', 'title',
            'pubdate','duration','view','danmaku','reply','favorite','coin','share','like']
    # Data
    data = pd.DataFrame(columns=name, data=videoData)
    # delete duplicates
    data = data.drop_duplicates()
    print(len(data))
    data.to_csv('data/yiqing_video_table.csv', encoding='utf-8', index=False)


if __name__ == '__main__':
    videoBvids = pd.read_csv('data/疫情视频.csv', encoding='gbk')['BV号'].to_list()
    videoDatas = []
    #videoBvids = videoBvids[:1]
    for videoBvid in videoBvids:
        # 实例化 Video 类
        videoData = []
        try:
            videoMsg = asyncio.get_event_loop().run_until_complete(getVideoMsg(bvid=videoBvid))
            videoTname = videoMsg['tname']
            videoTag = asyncio.get_event_loop().run_until_complete(getVideoTag(bvid=videoBvid))
            videoOwner_mid = videoMsg['owner']['mid']
            videoOwner_name = videoMsg['owner']['name']
            videoTitle = videoMsg['title']
            videoPubdate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(videoMsg["pubdate"]))
            videoTag_name = videoTag
            videoDuration = videoMsg['duration']
            videoStat = asyncio.get_event_loop().run_until_complete(getVideoStat(bvid=videoBvid))
            videoView = videoStat['view']
            videoDanmaku = videoStat['danmaku']
            videoReply = videoStat['reply']
            videoFavorite = videoStat['favorite']
            videoCoin = videoStat['coin']
            videoShare = videoStat['share']
            videoLike = videoStat['like']
            videoData.append(videoBvid)
            videoData.append(videoTname)
            videoData.append(videoTag_name)
            videoData.append(videoOwner_mid)
            videoData.append(videoOwner_name)
            videoData.append(videoTitle)
            videoData.append(videoPubdate)
            videoData.append(videoDuration)
            videoData.append(videoView)
            videoData.append(videoDanmaku)
            videoData.append(videoReply)
            videoData.append(videoFavorite)
            videoData.append(videoCoin)
            videoData.append(videoShare)
            videoData.append(videoLike)
            videoDatas.append(videoData)
            time.sleep(1)
        except ResponseCodeException:
            print('error')
            pass

    print(videoDatas)
    saveVideos(videoDatas)

