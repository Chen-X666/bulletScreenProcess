# _*_ coding: utf-8 _*_
"""
Time:     2022/2/11 19:54
Author:   ChenXin
Version:  V 0.1
File:     videoStatistic.py
Describe:  Github link: https://github.com/Chen-X666
"""
from collections import Counter

import matplotlib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

#
def videoRegularStatistic(inputPath=None):
    df = inputPath
    print(df.dtypes)
    # 数据正排序
    df = df.sort_values(by=['pubdate'])  # 降序排列
    df['pubdate'] = df['pubdate'].astype('datetime64[D]')
    df['pubYear'] = df["pubdate"].apply(
         lambda x: str(x).split("-")[0])
    df['pubMonth'] = df["pubdate"].apply(
         lambda x: str(x).split("-")[1])
    year_data = df['pubYear'].drop_duplicates().to_list()
    data = pd.DataFrame()
    for each_year_date in year_data:
        print(each_year_date)
        month_data = df[df["pubYear"] == each_year_date]['pubMonth'].to_list()
        tempData = pd.DataFrame.from_dict(Counter(month_data), orient='index').reset_index().rename(
            columns={'index': '发布月份', 0:'视频数量'})
        tempData['发布年份']=str(each_year_date).split("-")[0]
        print(tempData)
        data = pd.concat([data,tempData])
    data = data.reset_index()
    print(data)
    #data.to_csv('dongman.csv',index = False)
    data = pd.read_csv('dongman.csv')

    sns.set()
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['axes.unicode_minus'] = False
    palette = sns.color_palette("bright", len(set(data['发布年份'].to_list())))
    plot = sns.lineplot(x="发布月份", y="视频数量", data=data, hue="发布年份", palette=palette).figure.set_size_inches(6, 6)
    plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12])
    plt.show()

def videoBasicMsg(data):
    # 显示所有列 行
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    df = pd.DataFrame(data)
    print('{:-^60}'.format('数据基本情况'))
    print(df.head().append(df.tail()))
    print('{:-^60}'.format('数据基本统计分析'))
    print(df.describe())
    print('{:-^60}'.format('数据类型查看'))
    print(df.info())
    print('{:-^60}'.format('数据峰度查看；如果训练集和测试集分布不一致，就要考虑进行分布转换'))
    print('{:-^60}'.format('列 空值查看'))
    print(df.isnull().any(axis=0).sum())
    print('{:-^60}'.format('行 空值查看'))
    print(df.isnull().any(axis=1).sum())
    print('{:-^60}'.format('kurt查看'))
    print(df.kurt())

    print('{:*^60}'.format('相关系数分析:'))
    pd.reset_option("display.max_rows")  # 恢复默认设置
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['axes.unicode_minus'] = False
    data = data.rename(columns={'view': '观看量', 'danmaku':'弹幕量','reply': '转发量','favorite': '收藏量', 'coin': '投币量','share': '分享量', 'like': '喜欢量'})
    columns = ['观看量','弹幕量','转发量','收藏量','投币量','分享量','喜欢量']
    X_combine = pd.DataFrame(data[columns])
    corr = X_combine.corr().round(2)
    print(corr)  # 输出所有输入特征变量以及预测变量的相关性矩阵
    sns.heatmap(corr, cmap='Blues', annot=True)
    #sns.pairplot(data=X_combine.corr().round(2), diag_kind='kde')
    #sns.pairplot(data[data.columns])
    plt.show()

if __name__ == '__main__':
    df = pd.read_csv('data/videoData/guichu_video_table.csv', encoding='utf-8')
    #columns = ['view', 'danmaku', 'reply', 'favorite', 'coin', 'share', 'like','duration']
    videoBasicMsg(df)
    #videoDataStatistic(df)

