"""
爬取链家二手房信息
目标：爬取小区名称，总价
步骤：
１．url
    https://m.lianjia.com/gz/ershoufang/
2.正则匹配
３．写入本地文件
"""
# pymysql+pymongo
import requests
import re
import csv
class LianjiaSpider:
    def __init__(self):
        self.baseurl=".lianjia.com/ershoufang/pg"
        self.headers={"user-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1"}
        self.page=1

    def getPage(self,url,city):
        res=requests.get(url,headers=self.headers)
        res.encoding="utf-8"
        html=res.text
        self.parsePage(html,city)

    def parsePage(self,html,city):
        p=re.compile(r'<a.*?data-el="region">(.*?)</a>.*?<div class="totalPrice">.*?<span>(.*?)</span>',re.S)
        r_list=p.findall(html)
        print(r_list)
        self.writePage(r_list,city)
    #<div class="houseInfo">.*?<span class="houseIcon"></span>


    def writePage(self,r_list,city):
        with open("%s链家二手房.csv"%city,"a")as f:
            writer=csv.writer(f)
            for price in r_list:
                writer.writerow(price)

    def workOn(self):
        city = input("请输入您要下载城市的代码（例如：北京:bj;广州:gz）：")
        # number = input("请输入需要下载页面数：")
        while True:
            print("正在爬取%d页"%self.page)
            url="https://"+str(city)+self.baseurl+ str(self.page)+'/'
            self.getPage(url,city)
            print("第%d页爬取成功" % self.page)
            c=input("是否继续爬取(y/n)")
            if c.strip().lower()=="y":
                self.page+=1
            else:
                print("爬取结束，谢谢使用")
                break


if __name__=="__main__":
    spider=LianjiaSpider()
    spider.workOn()







