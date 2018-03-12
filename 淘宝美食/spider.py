# -*- coding:utf-8 -*-
from  selenium import webdriver
import selenium
import pymongo
import pymysql
from pyquery import PyQuery as pq
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re

import time
MONGO_URL = 'localhost'
MONGO_DB = 'taobao'
MONGO_TABLE = 'product'

SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']

KEYWORD = '美食'
browser = webdriver.Chrome()
# browser = webdriver.PhantomJS()
wait=WebDriverWait(browser,10)
browser.set_window_size(1400, 900)
def search():
    print('正在搜索')
    try:
     browser.get('https://www.taobao.com/')
     input=wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
     )
     submit=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
    #browser.find_element_by_xpath('//*[@id="q"]').send_keys('美食')
     input.send_keys(KEYWORD)
     submit.click()
     total = wait.until(
         EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
     print(total.text)

     get_product()

     return total.text
    except TimeoutException:
        return search()

def next_page(page_number):
    print('正在翻页', page_number)
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
        )
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_number)))
        time.sleep(5)

        get_product()

    except TimeoutException:
       next_page(page_number)

def get_product():
    time.sleep(5)

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    html=browser.page_source
    doc=pq(html)
    items=doc('#mainsrp-itemlist .items .item').items()

    for item in items:

        product={
            'image':'https://'+item.find('.pic .img').attr('src'),
            'price':item.find('.price').text(),
            'deal':item.find('.deal-cnt').text()[:-3],
            'title':item.find('.title').text(),
            'shop':item.find('.shop').text(),
            'location':item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)
def save_to_mongo(result):
    client = pymongo.MongoClient(MONGO_URL)
    db = client[MONGO_DB]
    try:
       if db[MONGO_TABLE].insert(result):
         print('成功', result)
    except Exception as e:
        print('失败',result)


def main():
    total=search()
    total=int(re.compile('(\d+)').search(total).group(1))
    for i in range(2,total+1):
        next_page(i)


if __name__ == '__main__':
    main()
