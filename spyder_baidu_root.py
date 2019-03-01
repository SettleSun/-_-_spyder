#!/usr/bin/python3
# coding: utf-8

import os
import sys
import requests
from bs4 import BeautifulSoup as bs
import pdb
import re
import threading
 
## 创建文件夹 保存爬的链接 保存数据      
IMG_DIR = "bigen_info"
if not os.path.exists(IMG_DIR):
    os.mkdir(IMG_DIR)
IMG_DIR = "data"
if not os.path.exists(IMG_DIR):
    os.mkdir(IMG_DIR)

def get_html_txt(url,id_view):
    session = requests.Session()
    session.headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'
        }  
    r = session.get(url)
    
    r.encoding = 'utf-8'
    soup = bs(r.text,'html.parser')
    #pdb.set_trace()
       # 当有多个class值时 解决办法：class值取其中之一
       ###   主题
    theme = soup.select('.main-content .lemmaWgt-lemmaTitle-title h1')[0].string# title 
    #if id_view % 20 == 0:print(url, " { |||||||||||| } ", theme)    

        ##  新建文件夹
    IMG_DIR1 = "./data/data_"+str(int(id_view/10000))+"/"
    if not os.path.exists(IMG_DIR1):
        os.mkdir(IMG_DIR1)
        
    file_write = open(IMG_DIR1+theme+".txt","w+",encoding='utf-8')
    #file_write.write(theme + ':\n')
    
    
    
        ###   内容
    content = soup.select('.main-content .para')#.string# title 
    for index,herf in enumerate(content):
        #name = herf.get("href")
        #txt_content = soup.get_text()
        ##save in a text file
        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub('', str(herf))
        dd = dd.strip().replace("\n", "")
        if dd == "":
            #print(index)
            continue
        file_write.write(dd + '\n')
        pass      
    pass
    file_write.close()
    

       
def run_spyder_baidu(bigen,end_info):    
    try:
        with open("./bigen_info/bigen_info_"+str(int(end_info/100000))+"_.txt") as bigen_info:        
            bigen = int(bigen_info.readline())-1
            #print(bigen,"  <<<<<<<<<<<<<<<<<<<<<")
    except:pass
    
    for id_view in range(end_info-bigen):
        try:
            url_baidu = "http://baike.baidu.com/view/"+str(id_view+bigen)+".htm"
            get_html_txt(url_baidu,id_view+bigen)
                     ##  写入当前网址  便于重启继续下载
            bigen_info = open("./bigen_info/bigen_info_"+str(int(end_info/100000))+"_.txt","w+",encoding='utf-8')    
            bigen_info.write(str(id_view+bigen))
            bigen_info.close()
            # break
        except:
            #print("\r\nURL error:",url_baidu,">>>>>>>>>>>>>>>>>>>>>>>>>>")
            pass
    print("》》》》》》》》》》》》》》》》》：",str(int(end_info/100000)))
##  多线程
class myThread (threading.Thread): # 继承父类threading.Thread

    def __init__(self, bigen, end_info):
        threading.Thread.__init__(self)
        self.bigen = bigen
        self.end_info = end_info
        
    def run(self): # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        run_spyder_baidu(self.bigen,self.end_info)
            
def main():
    for threadID in range(157):#0~156 0 0000 1557 5311   156 0 0000
        myThread(threadID*100000,threadID*100000+100000).start()
    pass
 
if __name__ == "__main__":
    main()
    #print("fanish>>>>>>>>>>>>>>main")


