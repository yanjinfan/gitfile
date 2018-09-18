# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ximalaya.items import XimalayaItem


class Wenxue2Spider(CrawlSpider):
    name = 'wenxue'
    allowed_domains = ['www.ximalaya.com']
    start_urls = ['https://www.ximalaya.com/youshengshu/wenxue/']
    #获取列表页的页码链接
    page_link = LinkExtractor(restrict_xpaths='//div[@class="pagination-wrap"]//a[@class="Yetd page-link"]')
    #获取详情页的页码链接
    detail_link = LinkExtractor(
        restrict_xpaths='//a[@class="HxMH album-title lg"]')
    rules = (
        #列表页只是打开页面，不获取数据
        Rule(page_link, follow=True),
        #详情页打开并获取数据
        Rule(detail_link, callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        #创建item对象
        item = XimalayaItem()
        #获取书名
        item['name'] = response.xpath('//h1/text()').extract_first()
        #获取主播名
        item['zbname'] = response.xpath('//p[@class="lqw4 anchor-info-nick"]/a/text()').extract_first()
        #获取书的地址
        item['baddr'] = response.url
        #获取章节列表
        chapter_list = response.xpath('//div[@class="dOi2 sound-list"]/ul//li')
        for chapter in chapter_list:
            #获取章节名
            item['cname'] = chapter.xpath('./div[@class="dOi2 text"]/a/text()').extract_first()
            #获取章节地址
            chapter_addr = chapter.xpath('./div[@class="dOi2 text"]/a/@href').extract_first()
            item['caddr'] = 'https://www.ximalaya.com' + chapter_addr
            #获取书的id
            item['bid'] = chapter_addr.split('/')[-2]
            #获取章节的id
            item['cid'] = chapter_addr.split('/')[-1]
            yield item
        #获取页码链接的列表
        page_list = response.xpath('//div[@class="dOi2 pagination"]//a[@class="Yetd page-link"]/@href').extract()
        for page in page_list:
            #拼接详情页的所有页码url
            page_url = 'https://www.ximalaya.com' + page
            #返回requset，并且调用parse_item获取所有页码的数据
            yield scrapy.Request(url=page_url, callback=self.parse_item)
