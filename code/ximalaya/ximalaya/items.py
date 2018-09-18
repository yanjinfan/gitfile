# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XimalayaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    '''
    - 书名- 主播名- 书的地址
    - 书的id
    - 章节名
    - 章节的id
    - 章节的地址（注意：不是下载地址）
    '''
    name = scrapy.Field()
    zbname = scrapy.Field()
    baddr = scrapy.Field()
    bid = scrapy.Field()
    cname = scrapy.Field()
    cid = scrapy.Field()
    caddr = scrapy.Field()