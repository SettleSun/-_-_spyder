from selenium import webdriver
import time
browser = webdriver.Firefox()

chrome_options = webdriver.ChromeOptions()
# 使用headless无界面浏览器模式
chrome_options.add_argument('--headless') #增加无界面选项
chrome_options.add_argument('--disable-gpu') #如果不加这个选项，有时定位会出现问题

# 启动浏览器，获取网页源代码
browser = webdriver.Chrome(executable_path=r'D:\Program Files (x86)\chromedriver.exe', chrome_options=chrome_options)

noAns = 0
def getAns(Q):
    global noAns
    mainUrl = "http://192.168.1.121:18805/cetc32_web/result?q="+Q
    browser.get(mainUrl)
    time.sleep(3)
    #print(f"browser text = {browser.page_source}")
    pageSource = browser.page_source
    with open("ans.txt","a+",encoding="utf-8") as ans:
        writeAns = pageSource.split("class=\"search-KBQA-list\"><div data-v-37172e7a=\"\">")[1].split("</div></div></div> <div data-v-37172e7a")[0].replace("</div> <div data-v-37172e7a=\"\">","")
        writeAns = writeAns.strip().replace(" ","")
        if len(writeAns.split(":")[2])==0:
            noAns += 1
        ans.write(writeAns + "\r\n================="+str(noAns)+"=======================\r\n")
        print(writeAns+"========678========================="+str(noAns)+"====================================================")

def readQ():
    with open("Q.txt") as Qs:
        while True:
            Q = next(Qs)
            getAns(Q)


if __name__ =="__main__":
    readQ()
    browser.quit()
