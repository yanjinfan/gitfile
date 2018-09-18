# -*- coding: utf-8 -*-
import json
import re
import jsonpath
import requests
import scrapy
from gupiao.items import GupiaoItem


class GpSpider(scrapy.Spider):
    name = 'gp'
    allowed_domains = ['quote.eastmoney.com', 'emweb.securities.eastmoney.com']
    start_urls = ['http://quote.eastmoney.com/center/gridlist.html#sz_a_board']

    def parse(self, response):
        # 获取股票代码列表
        code_list = response.xpath('//table[@id="main-table"]//tr/td[2]//text()').extract()
        for code in code_list:
            code_url = 'https://emweb.securities.eastmoney.com/PC_HSF10/CompanySurvey/CompanySurveyAjax?code=SZ' + code
            response = requests.get(code_url)
            obj = json.loads(response.text)
            # 创建item对象
            item = GupiaoItem()
            # 获取公司全称
            item['cname'] = jsonpath.jsonpath(obj, '$..gsmc')[0]
            # 获取A股代码
            item['code'] = jsonpath.jsonpath(obj, '$..agdm')[0]
            # 获取A股简称
            item['sname'] = jsonpath.jsonpath(obj, '$..agjc')[0]
            # 获取公司简介
            item['intro'] = jsonpath.jsonpath(obj, '$..gsjj')[0]
            # 获取经营范围
            item['business_scope'] = jsonpath.jsonpath(obj, '$..jyfw')[0]
            yield item