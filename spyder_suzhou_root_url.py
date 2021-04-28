# coding: utf-8

'''
base64验证码转图片：verification_code(login_source)
模拟登陆：login_suzhou()
获取href：get_page_urls()
获取txt：getInfo(url)
去掉重复的url：to_filter_out_duplicate()
'''
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import re
import csv
import numpy as np
import cv2 as cv
import base64

# browser = webdriver.Firefox()

chrome_options = webdriver.ChromeOptions()
# 使用headless无界面浏览器模式
chrome_options.add_argument('--headless')  # 增加无界面选项
chrome_options.add_argument('--disable-gpu')  # 如果不加这个选项，有时定位会出现问题

# 启动浏览器，获取网页源代码
browser = webdriver.Chrome(executable_path=r'/home/chan/IdeaProjects/study_daily/spider/chromedriver',
                           chrome_options=chrome_options)


def getInfo(url):
    '''
    详情页获取表格信息
    :param url:
    :return:
    '''

    browser.get(url)
    time.sleep(15)

    pageSource = browser.page_source
    title = browser.find_element_by_class_name('policy-info-detail-page__main__top__title')
    title_text = title.text
    try:  ## 没有内容直接返回
        table = browser.find_element_by_class_name('policy-info-detail-page__table')
    except:
        print("No：")
        return
    print("Ye：", title_text)
    table_texts = browser.find_elements_by_class_name("policy-info-detail-page__table__body__row__col")
    texts = []
    for txt in table_texts:
        texts.append(txt.text)
    # table_text = table.text
    # tables = table_text.split('\n')
    tablesn = np.reshape(texts, (-1, 4))
    with open("./CsvData/" + title_text + '.csv', 'w', encoding='utf-8-sig', newline='') as csf:
        writer = csv.writer(csf)
        for data in tablesn:
            writer.writerow(data[:3])


def verification_code(login_source):
    '''
    :param login_source:
    :return: 验证码，后期加OCR
    从HTML中获取base64的图片，转码并显示
    '''
    imgs = re.findall('(<img.*?>)', login_source)
    imgbase64s = re.findall('(,.*?")', imgs[1])
    imgbase64 = imgbase64s[0].replace(",", "").replace('"', "")
    ## base64转numpy array
    img_data = base64.b64decode(imgbase64)
    nparr = np.fromstring(img_data, np.uint8)
    img_np = cv.imdecode(nparr, cv.IMREAD_COLOR)
    # 显示图片，人工输入验证码
    cv.imshow('', img_np)
    cv.waitKey()
    cv.destroyAllWindows()
    veri_code = input("请输入验证码:")
    return veri_code


def login_suzhou():
    '''
    模拟输入登陆信息
    :return:
    '''
    url_login = r'https://www.qyfw.suzhou.com.cn/auth/login?redirect_uri=%2Fuser%2Frelation'
    browser.get(url_login)
    login_source = browser.page_source
    veri_code = verification_code(login_source)
    u = '正途皆是道'
    p = 'liutailin199210'
    browser.find_element_by_xpath('//*[@id="__layout"]/div/div/div/div[2]/form/div[1]/div/div[1]/input').send_keys(u)
    browser.find_element_by_xpath('//*[@id="__layout"]/div/div/div/div[2]/form/div[2]/div/div[1]/input').send_keys(p)
    browser.find_element_by_xpath('//*[@id="__layout"]/div/div/div/div[2]/form/div[3]/div/div/input').send_keys(
        veri_code)
    browser.find_element_by_xpath('//*[@id="__layout"]/div/div/div/div[2]/form/div[4]/div/button').click()  # 点击登陆
    time.sleep(5)

def get_page_urls(main_url):
    '''
    获取当前检索页中的url
    :return:
    '''
    browser.get(main_url)##主页
    time.sleep(5)
    urls = []
    for idss in range(50):
        print(idss)
        hrefs = browser.find_elements_by_xpath('//*[@id="__layout"]/div/div[3]/div/div[2]/div/div/main/a')
        for href in hrefs:
            url = href.get_attribute('href')
            with open("urls.txt",'a+',encoding="utf-8") as uf:
                uf.write(url+"\n")
            urls.append(url)
        ## 翻页
        browser.find_element_by_xpath('//*[@id="__layout"]/div/div[3]/div/div[2]/div/div/div[2]/div[1]/button[2]').click()
        time.sleep(5)
    return urls
def to_filter_out_duplicate():
    '''
    去掉重复的url
    :return:
    '''
    urls = []
    num = 0
    with open("urls_time.txt", encoding="utf-8") as uf:
        while 1:
            line = uf.readline()
            if not line:
                break
            url = line.strip()
            if url in urls:
                continue
            urls.append(url)
            num += 1
            print(num,url)

def app():
    '''
    1）登陆
    2）访问检索页
    3）获取检索页url
    4）访问url详情页获取  政策指标信息
    5）翻页
    重复345
    :return:
    '''
    ## 登陆页
    login_suzhou()
    ## 主页
    main_url = r'https://www.qyfw.suzhou.com.cn/zct-ee/policy-info?q=form~%7B%22policyType%22%3A%22%22%7C%22policySystem%22%3A%22%22%7C%22industryType%22%3A%22%22%7C%22area%22%3A%5B%5D%7C%22publishTimeRange%22%3A%5B%5D%7C%22applyTimeRange%22%3A%5B%5D%7C%22title%22%3A%222017%22%7D,sortProp~%7B%22orderField%22%3A%22%22%7C%22orderValue%22%3A%22%22%7D,pagination~%7B%22pageSize%22%3A10%7C%22total%22%3A500%7C%22currentPage%22%3A1%7C%22currentTotal%22%3A564%7D,control~%7B%22areaLevel%22%3A-1%7C%22searchTagItems%22%3A%5B%5D%7D,'

    urls = get_page_urls(main_url)
    for url in urls:
        ## 详情页
        getInfo(url)




if __name__ == "__main__":
    app()
    # ## 登陆页
    # login_suzhou()
    # ## 详情页
    # url = r"https://www.qyfw.suzhou.com.cn/zct-ee/policy-info/7675cfdb-0707-477b-8ccb-660aac98a6b9?channel=S"
    # getInfo(url)
    # browser.quit()
