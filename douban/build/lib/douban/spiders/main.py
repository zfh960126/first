# -*- coding: utf-8 -*-
__author__='douban'
from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(['scrapy','crawl','douban_book'])
execute(['scrapy','crawl','douban_comment'])
# execute(['scrapy','crawl','douban_mail'])
