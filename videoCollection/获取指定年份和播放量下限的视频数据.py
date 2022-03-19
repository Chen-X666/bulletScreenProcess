#-*- coding=utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import time
import win32api
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup

from videoCollection.疫情视频收集 import start_chrome

chrome_path='C:\Program Files\Google\Chrome\Application\chrome.exe'
chromedriver_path=r'C:\Users\Chen\Desktop\bulletProjects\bulletDataCollection\videoData\chromedriver.exe'
driver=start_chrome(chrome_path,chromedriver_path) #启动浏览器
driver.get('https://www.bilibili.com/v/channel/6400036?keyword=%E9%9D%A2%E7%AD%8B%E5%93%A5&tab=featured')

driver.implicitly_wait(30)
#2:2019
driver.find_elements_by_xpath("(//span[@class='year-selector__item'])")[3].click() #通过更换click前面的下标可以选择不同年份

def get_video(m):
    while True:
        time.sleep(0.2)
        win32api.keybd_event(34,0,0,0)  
        driver.implicitly_wait(30)
        video_card=driver.find_element_by_xpath("//ul[@class='card-list']").find_elements_by_xpath("//div[@class='video-card']")
        if float(re.match("(.*)万",video_card[-1].find_element_by_tag_name("span").text).group(1)) <= m:
            print(re.match("(.*)万",video_card[-1].find_element_by_tag_name("span").text).group(1))
            count=0
            for card in video_card[::-1]:
                video_play=card.find_element_by_tag_name("span").text #播放量
                if float(re.match("(.*)万",video_play).group(1)) >= m:
                    a=[]
                    b=[]
                    c=[]
                    d=[]
                    e=[]
                    f=[]
                    g=[]
                    for card in video_card[:count]:
                        video_play=card.find_element_by_tag_name("span").text #播放量
                        video_url = card.find_element_by_tag_name("a").get_attribute("href")  # 视频链接
                        video_bvno = video_url[31:]  # 视频bv号
                        video_name=card.find_element_by_css_selector(".video-name").text#视频名
                        video_user = card.find_element_by_css_selector(".up-name__text").text  # 发布人
                        video_length = card.find_element_by_css_selector(".play-duraiton").text  # 视频时长
                        video_like = card.find_element_by_css_selector(".like-text").text  # 点赞数
                        a.append(video_name)
                        b.append(video_play)
                        c.append(video_url)
                        d.append(video_bvno)
                        e.append(video_user)
                        f.append(video_length)
                        g.append(video_like)
                    driver.quit()
                    return a,b,c,d,e,f,g
                else:
                    count-=1
        else:
            continue

def get_date(bv_ids):
    video_dates=[]
    for av_id in bv_ids:
        print(av_id)
        # 获取时间 爬取视频页面html
        resp = requests.get(av_id)
        html = resp.text
        bf = BeautifulSoup(html, 'html.parser')
        bf1 = bf.find_all(class_='video-data')
        # 获取发布时间
        try:
            video_data = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})", str(bf1)).group(0)
        except AttributeError as e:
            print(e)
            video_data = 0

        video_dates.append(video_data)
    return video_dates


if __name__ == '__main__':
    a,b,c,d,e,f,g=get_video(35.1) #输入播放量下限（带小数点）
    h = get_date(c)
    pd.DataFrame({'video_bvno':d,'video_type':'AMV','video_name':a,'video_user':e,'video_date':h,'video_length':f,'video_play':b,'video_like':g,'video_url':c})\
        .drop_duplicates(subset=['video_bvno'])\
        .to_csv(r"面筋哥频道.csv",index=False,mode='a',encoding='utf-8-sig')
    