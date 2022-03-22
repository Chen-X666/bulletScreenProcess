# _*_ coding: utf-8 _*_
"""
Time:     2022/1/21 17:27
Author:   ChenXin
Version:  V 0.1
File:     videoTypeCollection.py
Describe:  Github link: https://github.com/Chen-X666
"""
import time

import win32api
from selenium import webdriver


def start_chrome(chrome_path,chromedriver_path): #启动Chrome浏览器
    options = webdriver.ChromeOptions()
    options.binary_location = chrome_path #浏览器路径
    chrome_driver_binary = chromedriver_path #driver路径
    driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options) #配置好参数给webdriver.Chrome，并用变量driver表示这个对象
    return driver

chrome_path='C:\Program Files\Google\Chrome\Application\chrome.exe'
chromedriver_path=r'C:\Users\Chen\Desktop\bulletProjects\bulletDataCollection\videoData\chromedriver.exe'
driver=start_chrome(chrome_path,chromedriver_path) #启动浏览器

for i in range(1,22):
    driver.get('https://www.bilibili.com/v/channel/type/'+str(i))
    driver.implicitly_wait(30)
    driver.find_elements_by_xpath('//*[@id="container"]/div/div[1]/span')[1].click()  # 通过更换click前面的下标可以选择不同年份
    while True:
        win32api.keybd_event(34, 0, 0, 0)
        driver.implicitly_wait(30)
        video_card = driver.find_element_by_xpath("//ul[@class='card-list']").find_elements_by_xpath(
            "//div[@class='video-card']")
