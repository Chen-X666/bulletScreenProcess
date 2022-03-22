# _*_ coding: utf-8 _*_
"""
Time:     2022/2/24 1:45
Author:   ChenXin
Version:  V 0.1
File:     bulletUserTrendStatistic.py
Describe:  Github link: https://github.com/Chen-X666
"""
from collections import Counter

import pandas as pd
def countBulletFront(df):
    df = df[df['dm_fontSize'] == 'True']
    df = df['dm_mode'].drop_duplicates()
    print(len(df))

def fontSize(df):
    count = Counter(df['dm_fontSize'].to_list())
    print(count)

if __name__ == '__main__':
    df = pd.read_csv('../bulletCollection/bullet_table_01.csv', encoding='utf-8')
    fontSize(df)
