# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class GupiaoPipeline(object):
    def __init__(self):
        # 在初始化的时候打开book.json
        self.fp = open('code.json', 'w', encoding='utf-8')
        # 拼接成列表格式，方便格式化
        self.fp.write('[')

    def process_item(self, item, spider):
        # 因为item只是看起来像字典，但其实不是字典，所以先把item转化成字典
        d = dict(item)
        # 转化成json格式
        s = json.dumps(d, ensure_ascii=False)
        # 写入数据，用逗号分割每条数据，方便格式化
        self.fp.write(s + ',')
        return item

    def close_spider(self, spider):
        # 拼接成列表格式，方便格式化
        self.fp.write(']')
        # 在爬虫结束的时候关闭文档
        self.fp.close()
