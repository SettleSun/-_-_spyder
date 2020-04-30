# coding: utf-8
import threading

from selenium import webdriver
import time
import re
import csv
import os
import winsound

rootUrl = r'https://www.ds78.xyz/'
browser = webdriver.Firefox()

chrome_options = webdriver.ChromeOptions()
# 使用headless无界面浏览器模式
chrome_options.add_argument('--headless') #增加无界面选项
chrome_options.add_argument('--disable-gpu') #如果不加这个选项，有时定位会出现问题

# 启动浏览器，获取网页源代码
browser = webdriver.Chrome(executable_path=r'D:\Program Files (x86)\chromedriver.exe', chrome_options=chrome_options)

def getInfo(mainUrl):
    time.sleep(3)
    browser.get(mainUrl)
    time.sleep(5)
    pageSource = browser.page_source
    ## 片子id
    ids = re.findall('(movie.php.*?")',pageSource)##地区
    ## 片子名称
    move_names = re.findall(r'(</script>.*?</a>)', pageSource) ##国家
    with open('moveInfo.csv', 'a+', encoding='utf-8-sig', newline='') as csf:
        for i in range(len(ids)):
            id = ids[i].replace('"',"")
            name = move_names[i].replace(r'</script>',"").replace(r"</a>","")
            data=[id,name]
            writer = csv.writer(csf)
            writer.writerow(data)

##  多线程
class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url


    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        getInfo(self.url)

if __name__ =="__main__":
    getInfo(rootUrl )
    #myThread(rootUrl).start()  # 多线程下载
    for i in range(2,50):
        ## https://www.ds26.xyz/index.php?page=3
        mainUrl = rootUrl+"index.php?page="+str(i)
        print(mainUrl)
        getInfo(mainUrl)
        #myThread(mainUrl).start()  # 多线程下载
        time.sleep(1)
    browser.quit()
    for i in range(2):
        winsound.Beep(600, 1000)
        time.sleep(1)



