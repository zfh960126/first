# -*- coding: utf-8 -*-
__author__='dongfangcaifu'
from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(['scrapy','crawl','eastmoney','-o','data1.csv'])
# execute(['scrapy','crawl','eastmoney-2','-o','data2.csv'])
# execute(['scrapy','crawl','eastmoney-3','-o','data3.csv'])
execute(['scrapy','crawl','eastmoney-4','-o','data4.csv'])