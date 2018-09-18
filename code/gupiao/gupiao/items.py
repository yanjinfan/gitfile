# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GupiaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    '''
    - 公司全称
    - A股代码
    - A股简称
    - 公司简介
    - 经营范围
    '''
    cname = scrapy.Field()
    code = scrapy.Field()
    sname = scrapy.Field()
    intro = scrapy.Field()
    business_scope = scrapy.Field()