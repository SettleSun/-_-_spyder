import random
import time

import PIL.Image as Image
import os
import sys
import requests
from bs4 import BeautifulSoup as bs
import threading
import re
from shutil import copyfile
import csv

import winsound
rootUrl = r'https://www.ds78.xyz/'



bigImgs = 'bigImgs'
if not os.path.exists(bigImgs):
    os.mkdir(bigImgs)
manyImgs = 'manyImgs'
if not os.path.exists(manyImgs):
    os.mkdir(manyImgs)
# 定义图像拼接函数
def image_compose(name):
    IMAGES_PATH = r'./manyImgs/'+name+r'/'  # 图片集地址
    IMAGES_FORMAT = ['.jpg', '.JPG']  # 图片格式
    IMAGE_SIZE = 256  # 每张小图片的大小
    IMAGE_ROW = 4  # 图片间隔，也就是合并成一张图后，一共有几行
    IMAGE_COLUMN = 4  # 图片间隔，也就是合并成一张图后，一共有几列
    IMAGE_SAVE_PATH = r'bigImgs/'+name+'.jpg'  # 图片转换后的地址
    # 获取图片集地址下的所有图片名称
    image_names = [name for name in os.listdir(IMAGES_PATH) for item in IMAGES_FORMAT if
                   os.path.splitext(name)[1] == item]
    img = Image.open(IMAGES_PATH+image_names[0])
    IMAGE_SIZEx,IMAGE_SIZEy=img.size
    # 简单的对于参数的设定和实际图片集的大小进行数量判断
    if len(image_names) != IMAGE_ROW * IMAGE_COLUMN:
        for imCopy in range(16-len(image_names)):
            copyfile(IMAGES_PATH+'p_1.jpg',IMAGES_PATH+"p_"+str(imCopy+len(image_names)+1)+'.jpg')
            pass
        #raise ValueError("合成图片的参数和要求的数量不能匹配！")
        image_names = [name for name in os.listdir(IMAGES_PATH) for item in IMAGES_FORMAT if
                   os.path.splitext(name)[1] == item]

    to_image = Image.new('RGB', (IMAGE_COLUMN * IMAGE_SIZEx, IMAGE_ROW * IMAGE_SIZEy))  # 创建一个新图
    # 循环遍历，把每张图片按顺序粘贴到对应位置上
    for y in range(1, IMAGE_ROW + 1):
        for x in range(1, IMAGE_COLUMN + 1):
            from_image = Image.open(IMAGES_PATH + image_names[IMAGE_COLUMN * (y - 1) + x - 1]).resize(
                (IMAGE_SIZEx, IMAGE_SIZEy), Image.ANTIALIAS)
            to_image.paste(from_image, ((x - 1) * IMAGE_SIZEx, (y - 1) * IMAGE_SIZEy))
    print("大图名称：",IMAGE_SAVE_PATH)
    return to_image.save(IMAGE_SAVE_PATH)  # 保存新图


def get_MainImg(url,avName):
    session = requests.Session()
    # 不同浏览器的UA
    header_list = [
        # 遨游
        {"user-agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)"},
        # 火狐
        {"user-agent": "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"},
        # 谷歌
        {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"}
    ]
    # 不同的代理IP
    proxy_list = [
        {"http": "112.115.57.20:3128"},
        {'http': '121.41.171.223:3128'}
    ]
    # 随机获取UA和代理IP
    header = random.choice(header_list)
    proxy = random.choice(proxy_list)
    r = requests.get(url=url, headers=header, proxies=proxy)
    if "<Response [404]>"==str(r):
        for i in range(2):
            winsound.Beep(600, 1000)
            #os.system("paplay BEEP1.WAV")
            time.sleep(1)
        raise ValueError("网页地址更改，请修改网页地址，并重启代码！")
    r.encoding = 'utf-8'
    soup = bs(r.text, 'html.parser')
    # 当有多个class值时 解决办法：class值取其中之一
    torrent = re.findall(r'(torrent/.*?.torrent)',str(soup.select('.download')[0]))[0]  # title
    saveTorrent(avName, torrent)

    imgSrcs = soup.select('img')  # title
    # <img src="/picture/48d90960262c9e3c115ee612584bb937b8fca414/thumb/00015.jpg" width="220">
    # imgSrcs = re.findall('(src=".*?jpg)',capture)
    dowmloadPicture(imgSrcs, avName)

def saveTorrent(avName,torrent):
    # 保存种子链接
    with open('torrent.csv', 'a+', encoding='utf-8-sig', newline='') as csf:
        data=[avName,torrent]
        writer = csv.writer(csf)
        writer.writerow(data)
def dowmloadPicture(imgUrls, avName):
    # 下载图片，超时重下
    num= 0
    for imgSrc in imgUrls:
        num += 1
        if 'picture' not in str(imgSrc):continue
        imgUrl = rootUrl + re.findall('(picture.*?jpg)',str(imgSrc))[0]
        print('正在下载第' + str(num ) + '张图片，图片地址:' + imgUrl)

        IMG_DIR = './manyImgs/' + avName
        if not os.path.exists(IMG_DIR):
            os.mkdir(IMG_DIR)
        string = './manyImgs/' + avName + '/p_' + str(num) + '.jpg'
        if os.path.exists(string):
            print("图片已经存在。。。。。。。。。。")
            continue
        d_n = 1
        while True:
            try:
                print('第_' + str(num) + '_张图片',"第：_",d_n,'_次下载。。。。')
                pic = requests.get(imgUrl, timeout=10)
                break
            except BaseException:
                print('第_'+str(d_n)+'_次下载错误，进行下一次下载')
                d_n += 1
                continue

        print("图片名称：",string)
        fp = open(string, 'wb')
        fp.write(pic.content)
        fp.close()

    image_compose(avName)
def validateTitle(title):
    # 去除非法字符
    rstr = r"[\/\\\:\*\?\"\<\>\|.， 。,]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title

def readCsv():
    IMAGES_PATH = r'./bigImgs/'  # 图片集地址
    IMAGES_FORMAT = ['.jpg', '.JPG']  # 图片格式
    image_names = [name for name in os.listdir(IMAGES_PATH) for item in IMAGES_FORMAT if
                   os.path.splitext(name)[1] == item]
    # 读取网页ID，断电继续上次ID下载
    with open('moveInfo.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        print(header)
        name = validateTitle(header[1])
        if name + '.jpg' not in image_names:
            id = re.findall('(movie.php.*)',str(header[0]))[0]
            url = rootUrl + id
            myThread(url, name).start()  # 多线程下载
        for data in reader:
            id = data[0]
            name = data[1]
            name = validateTitle(name)
            if name=="":#没有名称时，用ID替换名称
                name=re.findall('(id=.*)',id)[0].replace("id=","")
            if name+'.jpg' in image_names:
                print("资源已存在。。。。。")
                continue
            url = rootUrl + str(id)
            print("当前正在下载：", url)

            myThread(url, name).start()# 多线程下载
            #get_MainImg(url,name)# 单线程下载
            time.sleep(3)


##  多线程
class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, url, name):
        threading.Thread.__init__(self)
        self.url = url
        self.name = name

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        get_MainImg(self.url, self.name)

if __name__ == '__main__':
    readCsv()