import requests
import re
import csv
import pymysql
import warnings
class LianjiaSpider:
    def __init__(self):
        self.baseurl=".lianjia.com/ershoufang/pg"
        self.headers={"user-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1"}
        self.page=1
        #创建数据库连接对象
        self.db=pymysql.connect(host='localhost',
                   user='root',
                   port=3306,
                   password='123456',
                   charset="utf8")
        self.cursor=self.db.cursor()

    def getPage(self,url,city):
        res=requests.get(url,headers=self.headers)
        res.encoding="utf-8"
        html=res.text
        self.parsePage(html,city)

    def parsePage(self,html,city):
        p=re.compile(r'<a.*?data-el="region">(.*?)</a>.*?<div class="totalPrice">.*?<span>(.*?)</span>',re.S)
        r_list=p.findall(html)
        print(r_list)
        self.write_to_mysql(r_list)
    #<div class="houseInfo">.*?<span class="houseIcon"></span>

    #保存到ＭｙＳＱＬ数据库
    def write_to_mysql(self,r_list):
        c_db="create database if not EXISTS Lspider;"
        u_db="use Lspider;"
        c_tab="create table if not EXISTS lianjia(id int PRIMARY key auto_increment,name varchar(30),price DECIMAL(20,2))charset='utf8';"
        warnings.filterwarnings("error")
        try:
            self.cursor.execute(c_db)
        except Warning:
            pass

        self.cursor.execute(u_db)
        try:
            self.cursor.execute(c_tab)
        except Warning:
            pass

        for r_tuple in r_list:
            s_insert="insert into lianjia(name,price) VALUES ('%s','%s')"%(r_tuple[0].strip(),float(r_tuple[1].strip())*1000)
            self.cursor.execute(s_insert)
        print("第%d页数据存入成功"%self.page)


    def workOn(self):
        city = input("请输入您要下载城市的代码（例如：北京:bj;广州:gz）：")
        number = input("请输入需要下载页面数：")
        # while True:
        #     print("正在爬取%d页"%self.page)
        #     url="https://"+str(city)+self.baseurl+ str(self.page)+'/'
        #     self.getPage(url,city)
        #     print("第%d页爬取成功" % self.page)
        #     c=input("是否继续爬取(y/n)")
        #     if c.strip().lower()=="y":
        #         self.page+=1
        #     else:
        #         print("爬取结束，谢谢使用")
        #         break
        for page in range(1, int(number) + 1):
            url = "https://" + str(city) + self.baseurl + str(self.page) + '/'
            self.getPage(url, city)
            print("第%d页下载完成" % self.page)
            self.page += 1



if __name__=="__main__":
    SSpider=LianjiaSpider()
    SSpider.workOn()
