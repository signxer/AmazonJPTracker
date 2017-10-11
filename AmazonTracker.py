# 日亚价格监控
# Amazon JP Tracker
# 2017-10-10 23:43
# https://github.com/signxer/AmazonJPTracker
import re
import os
import time
import random
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
#---------------------------------------------------------------------
# 设置
#---------------------------------------------------------------------
#设定价格,低于此价格时发送微信
setPrice = 41500
#Server酱SCKEY (获取SCKEY：请注册一个GitHub账号，然后访问 https://sc.ftqq.com/?c=code，绑定完微信之后，把你的SCUKEY贴在下方，请保留引号)
sckey = "SCUxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
#追踪日亚商品网址，请保留引号
url = "https://www.amazon.co.jp/任天堂-Nintendo-Switch-スーパーマリオ-オデッセイセット/dp/B075LC4LK3/"
#价格检查间隔时间(秒)
timeInterval = 60
#错误重试间隔时间(秒)
errorInterval = 5
#---------------------------------------------------------------------
#提醒Title,如无特殊无需改动
title =  "日亚上架提醒"
#UA列表，如无特殊无需改动
user_agent_list = [\
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",\
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8",\
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",\
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",\
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",\
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",\
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",\
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",\
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:52.0) Gecko/20100101 Firefox/52.0",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36",\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36",\
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
       ]
#---------------------------------------------------------------------

def getPrice(url,user_agent_list):
    url = urllib.parse.quote(url,safe='/:?=+')
    ua = random.choice(user_agent_list)
    req = urllib.request.Request(
        url,
        data=None, 
        headers={
            'User-Agent': ua
        }
    )
    f = urllib.request.urlopen(req)
    soup = BeautifulSoup(f.read().decode('utf-8','ignore'), "lxml")
    data = soup.find('span',id="priceblock_ourprice")
    if data is None:
        return 0 #Error
    else:
        price = int(data.string[2:].replace(",",""))
        return price

def sendAlarm(title,content):
    alarmUrl = 'https://sc.ftqq.com/'+sckey+'.send?text='+urllib.parse.quote(title)+'&desp='+urllib.parse.quote(content)
    req = urllib.request.urlopen(alarmUrl)
    print(content)
    print("到达价格，发送微信提醒")

def main():
    while True:
        price = getPrice(url,user_agent_list)
        if(price == 0):
            print("获取价格失败，" + str(errorInterval) + "秒后重试")
            time.sleep(errorInterval)
        else:
            break
    localtime = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    content = localtime + " 当前价格为" + str(price)
    if price <= setPrice :
        content = content + ",已达到设定值" + str(setPrice) + ",买买买!"
        sendAlarm(title,content)
    else:
        content = content+ ",未达到设定值" + str(setPrice)
        print(content)
    time.sleep(timeInterval)

if __name__ == "__main__":
    while True:
        main()
