# -*- coding: UTF-8 -*-
# 以下为引用的一些Python包
from selenium import webdriver
import urllib.request
import os
import re
import time
import pandas as pd
# 以下为一些自定义的函数
from selenium.webdriver import ActionChains


def filename_filter(old_filename): # 非法文件名过滤，非法字符转为空格
    import re
    new_filename=re.sub(r'[\\/:*?"<>|\r\n]+', " ", old_filename)
    return new_filename

def start_chrome(chrome_path,chromedriver_path): #启动Chrome浏览器
    options = webdriver.ChromeOptions()
    options.binary_location = chrome_path #浏览器路径
    chrome_driver_binary = chromedriver_path #driver路径
    driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options) #配置好参数给webdriver.Chrome，并用变量driver表示这个对象
    return driver

def getKeyWord():
    keywords = pd.read_csv('data/keyword.csv')['keyword'].to_list()
    return keywords


# 代码执行区域
if __name__ == "__main__":
    videoList = []
    chrome_path='C:\Program Files\Google\Chrome\Application\chrome.exe'
    chromedriver_path=r'C:\Users\Chen\Desktop\bulletAnalysis\DataCollection\chromedriver.exe'
    driver=start_chrome(chrome_path,chromedriver_path) #启动浏览器
    #driver = webdriver.Firefox()
    """代码部分"""
    data = pd.DataFrame({"BV号":[],"弹幕量":[]})
    count = 0
    for keyword in getKeyWord():
        url = "https://search.bilibili.com/all?keyword="+keyword+"&from_source=webtop_search&spm_id_from=333.1007&order=dm&duration=0&tids_1=0"
        judge = True
        page = 0
        while judge:
            page = page+1
            driver.get(url+"&page="+str(page))
            double_click = driver.find_element_by_xpath(
                '/html/body/div[3]/div/div[2]/div/div[1]/div[1]/div[1]/div[2]')  # 百度一下
            ActionChains(driver).double_click(double_click).perform()
            time.sleep(1)

            for vt in driver.find_elements_by_xpath("//li[@class='video-item list']"):
                bv = vt.find_element_by_tag_name("a").get_attribute("href")
                bv = re.match('.*(BV.*)\?.*',bv).group(1)
                watch_num = vt.find_element_by_xpath(".//span[@title='弹幕']").text
                print(watch_num)
                if re.match("(.*)万",watch_num):
                    if float(re.match("(.*)万",watch_num).group(1)) >= 1.0:
                        print(bv,watch_num)
                        data = data.append(pd.Series({"BV号":bv,"弹幕量":watch_num},name=count))
                        videoList.append(bv)
                        count+=1
                else:
                    judge = False
        print(data)
        data.to_csv('疫情视频.csv',index=False,mode="a+",encoding='gbk')
    """代码部分"""
            
            