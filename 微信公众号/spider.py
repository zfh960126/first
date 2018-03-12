# -*- coding:utf-8 -*-
import threading
from threading import Thread
from time import ctime,sleep

import requests
from urllib.parse import urlencode
from requests.exceptions import ConnectionError
from pyquery import PyQuery as pq
import pymongo
import xlwt


KEYWORD = 'java'
client = pymongo.MongoClient('localhost')
db = client['weixin']

base_url = "http://weixin.sogou.com/weixin?"

headers = {
    'Cookie': 'SUV=00BC2C44D3947A845A2A953A3B1CB132; CXID=2D9938ACBCFB91CF942B687BE867A006; sw_uuid=3250458409; sg_uuid=6130781207; dt_ssuid=4457624775; pex=C864C03270DED3DD8A06887A372DA219231FFAC25A9D64AE09E82AED12E416AC; ssuid=5436058204; IPLOC=CN4403; OPENID=003C7C83F6B45B7B0738188B1AEABC09; ad=alllllllll2zuTRRlllllV$kehGlllllTJ0kEkllll9llllljllll5@@@@@@@@@@; SUID=CE61C50E4B238B0A5A35E880000EEEC2; YYID=ED7751013372F15741E6CA839EC239A9; ABTEST=0|1520734087|v1; SNUID=E4EB93D70B0E6D12741049A50BF27D63; __guid=14337457.1987485461632127200.1520734096536.723; JSESSIONID=aaaYEIPQM_DhjaMa1ryhw; monitor_count=7',
    'Host': 'weixin.sogou.com',
    'Referer': 'http://weixin.sogou.com/antispider/?from=%2fweixin%3Fquery%3d%E9%A3%8E%E6%99%AF%26_sug_type_%3d%26s_from%3dinput%26_sug_%3dn%26type%3d2%26page%3d99%26ie%3dutf8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'

}


proxy_url = "http://127.0.0.1:5000/get"
proxy = None
max_count = 5
class WeixinArtical():

    def __init__(self,keyword,page):
        self.keyword = keyword
        self.page = page

        self.run(keyword,page)


    def get_proxy(self):
        try:
            response = requests.get(proxy_url)
            if response.status_code == 200:
                print(response.text)
                return response.text
            return None
        except ConnectionError:
            return None


    def get_html(self,url, count=1):
        print ('url', url)
        print ('count', count)
        global proxy
        if count >= max_count:
            print ('Tried too many counts')
            return None
        try:
            if proxy:
                proxies = {
                    'http': 'http://' + proxy,
                }
                response = requests.get(url, allow_redirects=False, headers=headers, proxies=proxies)
            else:
                response = requests.get(url, allow_redirects=False, headers=headers)
            # allow_redirects=False:不进行自动跳转
            if response.status_code == 200:
                return response.text
            if response.status_code == 302:
                # Need Proxy
                print ('302')
                proxy = self.get_proxy()
                if proxy:
                    print ('Useing proxy',proxy)
                    return self.get_html(url)
                else:
                    print ('Get Proxy Failed')
                    return None
        except ConnectionError as e:
            print ('Error Occured', e.args)
            proxy = self.get_proxy()
            count += 1
            return self.get_html(url,count)



    def get_index(self,keyword, page):
        data = {
            "query": keyword,
            "type": 2,
            "page": page,
        }
        queries = urlencode (data)
        url = base_url + queries
        print(url)
        html = self.get_html(url)
        return html


    def parse_index(self,html):
        doc = pq(html)
        items = doc('.news-box .news-list li .txt-box h3 a').items()
        for item in items:
            yield item.attr('href')


    def get_detail(self,url):
        try:
            response = requests.get(url)

            if response.status_code == 200:
                return response.text
            return None
        except ConnectionError:
            return None


    def pase_detail(self,html):
        try:
            doc = pq(html)
            title = doc('.rich_media_title').text()
            content = doc('.rich_media_content').text()
            date = doc("#post-data").text()
            nickname = doc('.rich_media_meta_list .rich_media_meta_nickname').text()
            wechat = doc('#post-user').text()
            return {
                'title': title,
                'content': content,
                'date': date,
                'nickname': nickname,
                'wechat': wechat,
            }
        except XMLSyntaxError:
            return None

    def save_to_mongo(self,data):
        if db['articles'].update({'title':data['title']},{'$set':data},True):
            print ('save to mongo', data['title'])
        else:
            print ('save to mongo fail')





    def run(self,keyword,max_page):
        for page in range(1, max_page):
            html = self.get_index(keyword, page)
            if html:
                article_urls = self.parse_index(html)
                for article_url in article_urls:
                    article_html = self.get_detail(article_url)
                    if article_html:
                        article_data = self.pase_detail(article_html)
                        #print (article_data)
                        self.save_to_mongo(article_data)

class MyThread(Thread):
    def __init__(self,keyword,page):
        Thread.__init__(self)
        self.keyword = keyword
        self.page = page

    def run(self):
        WeixinArtical(self.keyword,self.page)

threads = []
if __name__ == '__main__':
    for i in range(1,100):
        t = MyThread(KEYWORD,i)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

