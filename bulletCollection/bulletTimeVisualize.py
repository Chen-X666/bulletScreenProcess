# _*_ coding: utf-8 _*_
"""
Time:     2022/1/10 17:52
Author:   ChenXin
Version:  V 0.1
File:     bulletTimeVisualize.py
Describe:  Github link: https://github.com/Chen-X666
"""
import time
from collections import Counter
from sklearn.preprocessing import scale
import matplotlib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def Z_Score(data):
    lenth = len(data)
    total = sum(data)
    ave = float(total)/lenth
    tempsum = sum([pow(data[i] - ave,2) for i in range(lenth)])
    tempsum = pow(float(tempsum)/lenth,0.5)
    for i in range(lenth):
        data[i] = (data[i] - ave)/tempsum
    return data

def processTime(df,column):
    #pandas 返回的是格林威治标准时间，与北京时间差了 8 小时
    df[column]=pd.to_datetime(df[column],unit='s', origin='1970-01-01 08:00:00')
    return df

def innerTimeVisualize(inputPath):
    input = pd.read_csv('../bulletCollection/data/面筋哥_bullet_table.csv', encoding='utf-8')
    input = input[input['bvno'] == 'BV1GW411g7mc']
    print(input)
    # 降序排列
    input = input.sort_values(by=['dm_time'])
    # 按秒分
    input["dm_time"] = input["dm_time"].apply(
        lambda x: str(x).split(".")[0])
    videoTime_data = input["dm_time"].drop_duplicates()
    videoTime_group = input.groupby(["dm_time"])
    x_axis = []
    y_axis = []
    for each_videoTime in videoTime_data:
        data_each_day = videoTime_group.get_group(each_videoTime)
        x_axis.append(int(float(each_videoTime)))
        y_axis.append(len(data_each_day))
    sns.set()
    sns.lineplot(x=x_axis, y=y_axis)

    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['axes.unicode_minus'] = False
    plt.xticks(np.arange(min(x_axis), max(x_axis), (max(x_axis) - min(x_axis)) / 10))

    plt.xlabel("视频时间(单位：秒)")

    plt.ylabel("弹幕数量")
    plt.show()



def outterTimeVisualize(inputPath):
    inputs = pd.read_csv('../bulletCollection/data/yq2019-12-01_2020-12-01.csv', encoding='utf-8')
    print(inputs.dtypes)
    inputs['sendTime'] = inputs['sendTime'].astype('int64')
    print(len(inputs))
    # 数据正排序
    inputs = inputs.sort_values(by=['sendTime'])  # 降序排列
    # 时间搓转换
    inputs = processTime(inputs, 'sendTime')
    inputs = inputs[inputs['sendTime'] <= '2020-12-01']
    # 把time列的日期时间根据 空格符
    inputs["sendTime"] = inputs["sendTime"].apply(
        lambda x: str(x).split(" ")[0])
    # 获得不重复的天
    # day_data = inputs["dm_sendTime"].drop_duplicates()
    # day_group = inputs.groupby(["dm_sendTime"])

    # for each_day in day_data:
    #     data_each_day = day_group.get_group(each_day)
    #     x_axis.append(each_day)
    #     y_axis.append(len(data_each_day))
    day_data = inputs["sendTime"].to_list()
    data = pd.DataFrame.from_dict(Counter(day_data), orient='index').reset_index().rename(
        columns={'index': '弹幕日期', 0: '弹幕数量'}).set_index('弹幕日期')
    print(data)
    dateRange = pd.date_range(start='2019-12-01', end='2020-12-01')
    data = data.reindex(dateRange)
    print(data)
    data['弹幕数量'] = data['弹幕数量'].fillna(0)
    print(data)
    data.to_csv('data/sendTimeData.csv',encoding='utf-8')
    sns.set()
    sns.lineplot(x=data.index, y='弹幕数量', data=data).figure.set_size_inches(16, 6)
    plt.gcf().autofmt_xdate()

    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['axes.unicode_minus'] = False
    # plt.xticks(['2019-12-16','2018-12-17',
    #             '2019-12-18','2019-05-01',
    #             '2020-01-01','2020-06-01',
    #             '2020-12-01'])

    #plt.xticks(np.arange(min(x_axis),max(x_axis),(max(x_axis)-min(x_axis))/5))
    # get current axis
    plt.xlabel('日期时间')

    plt.show()

def countTimeData(filePath,timeColumn,startTime,endTime,numColumn):
    df = pd.read_csv(filePath,encoding='utf-8')
    df = df[(df[timeColumn]>=startTime)&(df[timeColumn]<=endTime)]
    print(sum(df[numColumn].to_list()))
    return sum(df[numColumn].to_list())


def twoDimensionTimeVisualize():
    # input = pd.read_csv('../bulletCollection/data/面筋哥_bullet_table.csv', encoding='utf-8')
    # input = input[input['bvno'] == 'BV1GW411g7mc']
    # # 降序排列
    # input = input.sort_values(by=['dm_time'])
    # # 按秒分
    # input["dm_time"] = input["dm_time"].apply(
    #     lambda x: str(x).split(".")[0])
    # input = input.sort_values(by=['dm_sendTime'])  # 降序排列
    # input = processTime(input, 'dm_sendTime')
    # input["dm_sendTime"] = input["dm_sendTime"].apply(
    #     lambda x: str(x).split(" ")[0])
    # print(input)
    #
    # #videoTime_data = input["dm_time"].drop_duplicates()
    # date_data = input["dm_sendTime"].drop_duplicates().to_list()
    # # videoTime_group = input.groupby(["dm_time","dm_sendTime"])
    # # print(videoTime_group)
    # print(date_data)
    # print(input)
    # data = pd.DataFrame(columns=['视频时间','弹幕数量','日期时间'])
    # for each_dateTime in date_data:
    #     print(each_dateTime)
    #     tempData = input[input['dm_sendTime']==each_dateTime]
    #     videoTime_data = tempData["dm_time"].to_list()
    #     tempData = pd.DataFrame.from_dict(Counter(videoTime_data), orient='index').reset_index().rename(
    #         columns={'index': '视频时间', 0: '弹幕数量'})
    #     tempData['日期时间'] =each_dateTime
    #     print(tempData)
    #     data = pd.concat([data,tempData],ignore_index=True)
    # data.reset_index().to_csv('1.csv')
    input = pd.read_csv('1.csv')
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    import seaborn as sns
    input = input.sort_values(by=['日期时间','视频时间'])  # 降序排列
    input['日期时间'] = input['日期时间'].apply(lambda x: time.mktime(time.strptime(x, '%Y-%m-%d')))
    print(input)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_trisurf(input['日期时间'], input['视频时间'], input['弹幕数量'], cmap=plt.cm.viridis, linewidth=0.2)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()


if __name__ == '__main__':
    twoDimensionTimeVisualize()
    #innerTimeVisualize(inputPath=None)
    #outterTimeVisualize(inputPath=None)
    #countTimeData(filePath='data/sendTimeData.csv',timeColumn='sendTime',numColumn='num',startTime='2020-05-01',endTime='2020-06-01')

