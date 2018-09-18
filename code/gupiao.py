import json
import time
import jsonpath
import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 创建option对象
chrome_options = Options()
# 设置无头浏览器的参数
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
# driver路径
path = '/Users/yanjinfan/Desktop/python/crawler/code/chromedriver'
# 创建浏览器对象
browser = webdriver.Chrome(executable_path=path)
# 访问指定网址
browser.get('http://quote.eastmoney.com/center/gridlist.html#sz_a_board')
time.sleep(3)
# 获取最大页码
max_page = int(browser.find_element_by_xpath('//a[@class="paginate_button"][last()]').text)
company_info = []
# 遍历每一页
for page in range(1, max_page + 1):
    print(page)
    # 当页码大于1的时候，在输入页码的输入框输入页码，并点击提交
    if page > 1:
        # 获取输入页码的输入框
        page_input = browser.find_element_by_xpath('//input[@class="paginate_input"]')
        # 清除输入框的数据
        page_input.clear()
        # 输入页码
        page_input.send_keys(page)
        # 获取点击跳转页码的按钮
        btn = browser.find_element_by_xpath('//a[@class="paginte_go"]')
        # 点击跳转页码的按钮
        btn.click()
        time.sleep(3)
    # 创建etree对象
    etree_obj = etree.HTML(browser.page_source)
    # 获取股票代码
    code_list = etree_obj.xpath('//table[@id="main-table"]//tr/td[2]//text()')
    # 遍历每个股票代码
    for code in code_list:
        # 拼接url
        url = 'https://emweb.securities.eastmoney.com/PC_HSF10/CompanySurvey/CompanySurveyAjax?code=SZ' + code
        # 获取json数据
        res = requests.get(url=url)
        # 加载json数据
        obj = json.loads(res.text)
        # 获取公司全称
        cname = jsonpath.jsonpath(obj, '$..gsmc')[0]
        # 获取A股简称
        sname = jsonpath.jsonpath(obj, '$..agjc')[0]
        # 获取公司简介
        intro = jsonpath.jsonpath(obj, '$..gsjj')[0]
        # 获取经营范围
        business_scope = jsonpath.jsonpath(obj, '$..jyfw')[0]
        # 把数据放在字典中
        company = {
            '公司全称': cname,
            'A股代码': code,
            'A股简称': sname,
            '公司简介': intro,
            '经营范围': business_scope
        }
        print(company)
        # 把每一条数据放到列表中
        company_info.append(company)
# 退出浏览器
browser.quit()
# 把数据转化为Json数据
src = json.dumps(company_info)
# 写入到本地
with open('code.json') as fp:
    fp.write(src)
