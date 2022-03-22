# _*_ coding: utf-8 _*_
"""
Time:     2021/8/28 14:59
Author:   ChenXin
Version:  V 0.1
File:     频数SentenceLong.py
Describe:  Github link: https://github.com/Chen-X666
"""
import re
from collections import Counter

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import pandas
import matplotlib as mpl
import pandas as pd
import jieba

def drawPic(x):
    import seaborn as sns
    plt.style.use('ggplot')
    import matplotlib
    sns.set()
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['axes.unicode_minus'] = False
    palette = sns.color_palette("bright", len(set(x['语料库类型'].to_list())))
    sns.lineplot(x="弹幕字串长度", y="频数",  data=x,palette=palette,hue='语料库类型')
    plt.xticks([1,2,3,4, 6, 8,10,20,30,40,50])
    plt.show()

def staticWord(filePaths, bulletTypes, column):
    Slong = pd.DataFrame()
    for filePath, bulletType in zip(filePaths, bulletTypes):
        Slong1 = []
        text = pd.read_csv(filePath, encoding='utf-8')[column].to_list()
        for i in text:
            Slong1.append(len(jieba.lcut(str(i))))
        print(Counter(Slong1))
        Slong1 = pd.DataFrame.from_dict(Counter(Slong1), orient='index').reset_index().rename(
            columns={'index': '弹幕词语数量', 0: '频数'})
        Slong1.loc['new'] = [0, 0]
        Slong1['语料库类型'] = bulletType
        Slong = pd.concat([Slong, Slong1])
        print(Slong)
    Slong = Slong.reset_index(drop=True)
    Slong = Slong[Slong['弹幕词语数量'] <= 50]
    return Slong

def staticChar(filePaths, bulletTypes, column):
    Slong = pd.DataFrame()
    for filePath, bulletType in zip(filePaths, bulletTypes):
        Slong1 = []
        text = pd.read_csv(filePath,encoding='gbk')[column].to_list()
        for i in text:
            #print(i)
            Slong1.append(len(str(i)))
        print(Counter(Slong1))
        Slong1 = pd.DataFrame.from_dict(Counter(Slong1), orient='index').reset_index().rename(
            columns={'index': '弹幕字串长度', 0: '频数'})
        Slong1.loc['new'] = [0, 0]
        Slong1['语料库类型'] = bulletType
        Slong = pd.concat([Slong, Slong1])
        print(Slong)
    Slong = Slong.reset_index(drop=True)
    Slong = Slong[Slong['弹幕字串长度'] <= 50]
    return Slong


def get_words(txt):
    seg_list = jieba.cut(txt)
    c = Counter()
    for x in seg_list:
        if len(x) > 1 and x != '\r\n':
            c[x] += 1
    print('常用词频度统计结果')
    for (k, v) in c.most_common(50):
        print('%s%s %s  %d' % ('  ' * (5 - len(k)), k, '*' * int(v / 2), v))


if __name__ == '__main__':
    filenames = ['../bulletCollection/data/BV1m7411F7si.csv']
    bulletTypes = ['疫情弹幕语料库']
    Slong = staticChar(filePaths=filenames, bulletTypes=bulletTypes,column='dm_text')
    print(Slong)
    drawPic(Slong)





