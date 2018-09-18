# -*- coding: utf-8 -*-
import scrapy

from jdproject.items import JdprojectItem


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['item.jd.com']
    start_urls = ['https://huawei.jd.com/']

    def parse(self, response):
        #获取手机列表
        mobile_list = response.xpath('//div[@class="goods-img"]/a')
        for mobile in mobile_list:
            #获取手机详情页的url
            mobile_url = 'https:' + mobile.xpath('./@href').extract_first()
            #返回request，url访问手机详情页，调用parse_detail获取数据
            yield scrapy.Request(url=mobile_url, callback=self.parse_detail)

    def parse_detail(self, response):
        #创建item对象
        item = JdprojectItem()
        #判断字符串是否为空
        def not_empty(s):
            return s and s.strip()
        #获取价格
        item['price'] = response.xpath('//span[@class="p-price"]/span[2]/text()').extract_first()
        #获取促销信息1
        promotion1 = response.xpath('//div[@class="prom-gifts clearfix"]//text()').extract()
        #获取促销信息2
        promotion2 = response.xpath('//div[@class="J-prom-quan prom-quan"]//text()').extract()
        #将促销信息1拼接成字符串，并去除多余空格
        promotion1 = ' '.join(list(filter(not_empty, promotion1)))
        #将促销信息拼接起来
        item['promotion'] = promotion1 + ''.join(promotion2)
        #获取增值业务
        item['vas'] = ' '.join(response.xpath('//div[@id="summary-support"]/div[2]//span/text()').extract())
        #获取重量
        item['weight'] = response.xpath('//div[@id="summary-weight"]/div[2]/text()').extract_first()
        #获取选择颜色
        item['color'] = ' '.join(response.xpath('//div[@id="choose-attr-1"]//i/text()').extract())
        #获取选择版本
        edition = response.xpath('//div[@id="choose-attr-2"]//a/text()').extract()
        edition_src = ''
        #去除空格拼接成字符串
        for ed in edition:
            edition_src += ed.strip() + ','
        item['edition_src'] = edition_src
        #获取购买方式
        item['buy'] = ' '.join(response.xpath('//div[@id="choose-type"]//a/text()').extract())
        #获取套装
        item['suit'] = ' '.join(response.xpath('//div[@id="choose-suits"]//a/text()').extract())
        #获取增值保障
        server = ' '.join(response.xpath('//div[@id="choose-service"]//span/text()').extract())
        server_src = ''
        # 去除空格拼接成字符串
        for s in server:
            server_src += s.strip()
        item['server_src'] = server_src + ','
        #获取白条分期
        baitiao = ' '.join(response.xpath('//div[@id="choose-baitiao"]//strong/text()').extract())
        baitiao_src = ''
        # 去除空格拼接成字符串
        for b in baitiao:
            baitiao_src += b.strip()
        item['baitiao_src'] = baitiao_src + ','
        yield item
