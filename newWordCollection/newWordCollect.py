# _*_ coding: utf-8 _*_
"""
Time:     2021/11/29 22:23
Author:   ChenXin
Version:  V 0.1
File:     newWordCollect.py
Describe:  Github link: https://github.com/Chen-X666
"""
from selenium import webdriver
import urllib.request
import os
import re
import time
import pandas as pd


def start_chrome(chrome_path,chromedriver_path): #启动Chrome浏览器
    options = webdriver.ChromeOptions()
    options.binary_location = chrome_path #浏览器路径
    chrome_driver_binary = chromedriver_path #driver路径
    driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options) #配置好参数给webdriver.Chrome，并用变量driver表示这个对象
    return driver

if __name__ == '__main__':
    newWord = []
    chrome_path = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
    chromedriver_path = r'C:\Users\Chen\Desktop\bulletAnalysis\DataCollection\chromedriver.exe'
    driver = start_chrome(chrome_path, chromedriver_path)  # 启动浏览器
    for i in range(1,24,1):
        url = 'https://gengbaike.cn/category-view-13-' + str(i) + '.html'
        print(url)
        driver.get(url)
        for j in range(1,21):
            xpath = '/html/body/section/div/dl[' + str(j) + ']/dt/a'
            e = driver.find_element_by_xpath(xpath).text
            print(e)
            newWord.append(e)
    driver.close()
    pd.DataFrame(newWord).to_csv('newWord.csv',encoding='utf-8',index=False)




