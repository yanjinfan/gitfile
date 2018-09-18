# #*# coding: utf#8 #*#

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 京东价
    price = scrapy.Field()
    # 促销
    promotion = scrapy.Field()
    # 增值业务
    vas = scrapy.Field()
    # 重量
    weight = scrapy.Field()
    # 选择颜色
    color = scrapy.Field()
    # 选择版本
    edition_src = scrapy.Field()
    # 购买方式
    buy = scrapy.Field()
    # 套装
    suit = scrapy.Field()
    # 增值保障
    server_src = scrapy.Field()
    # 白条分期
    baitiao_src = scrapy.Field()