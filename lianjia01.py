from urllib import request

import re
import random
# from day02.useragents import ua_list
import csv
import ssl
import time

# ssl._create_default_https_context = ssl._create_unverified_context


class SpyderLianjia:
    def __init__(self):
        self.url = ".lianjia.com/ershoufang/pg"
        self.page = 1
        self.headers = {
            "user-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1"}

    def getPage(self, url,city):
        req = request.Request(url, headers=self.headers)
        # print(random.choice(ua_list))
        res = request.urlopen(req)
        html = res.read().decode("utf-8")
        # print(html)
        self.parsePage(html,city)

    def parsePage(self, html,city):
        p = re.compile(
            '<div class="houseInfo">.*?<span class="houseIcon"></span>.*?data-el="region">(.*?)</a>.*?<div class="totalPrice">.*?<span>(.*?)</span>',
            re.S)
        # p = re.compile('云山诗意',re.S)
        # .*?<div class="totalPrice">.*?<span>(>*?)</span>
        price_list = p.findall(html)
        print(price_list)
        self.writePage(price_list,city)

    def writePage(self, price_list,city):
        with open("%s.csv"%city, "a") as f:
            writer = csv.writer(f)
            for price in price_list:
                writer.writerow(price)
                # L = [
                #     price[0].strip(),
                #     price[1].strip(),
                # ]

    def main(self):
        city = input("请输入您要下载城市的代码（例如：北京:bj;广州:gz）：")
        number = input("请输入需要下载页面数：")

        # https: // bj.lianjia.com / ershoufang / pg2 /
        for page in range(1, int(number) + 1):
            url = "https://" + str(city) + self.url + str(page) + "/"
            print(url)

            self.getPage(url,city)
            time.sleep(0.5)
            print("第%d页下载完成" % self.page)
            self.page += 1


if __name__ == "__main__":
    spyder = SpyderLianjia()
    spyder.main()
