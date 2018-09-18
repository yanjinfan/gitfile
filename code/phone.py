import json
import time
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

'''
- 京东价
- 促销
- 增值业务
- 重量 
- 选择颜色
- 选择版本
- 购买方式 
- 套装 
- 增值保障
- 白条分期
'''
# 创建option对象
chrome_options = Options()
# 添加无头浏览器参数
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
# 设置要访问的网址
url = 'https://item.jd.com/5826236.html'
# 设置driver路径
path = '/Users/yanjinfan/Desktop/python/crawler/code/chromedriver'
# 创建浏览器对象
browser = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
# 用浏览器访问要访问的网址
browser.get(url)
time.sleep(3)
# 创建etree对象
etree_obj = etree.HTML(browser.page_source)


# 去除空字符串
def not_empty(s):
    return s and s.strip()


# 获取价格
price = etree_obj.xpath('//span[@class="p-price"]/span[2]/text()')[0]
# 获取促销数据1
promotion1 = etree_obj.xpath('//div[@class="prom-gifts clearfix"]//text()')
# 获取促销数据2
promotion2 = etree_obj.xpath('//div[@class="J-prom-quan prom-quan"]//text()')
# 拼接促销信息
promotion1 = ''.join(list(filter(not_empty, promotion1)))
promotion = promotion1 + ''.join(promotion2)
# 获取增值业务
vas = ''.join(etree_obj.xpath('//div[@id="summary-support"]/div[2]//span/text()'))
# 获取重量
weight = etree_obj.xpath('//div[@id="summary-weight"]/div[2]/text()')[0]
# 获取选择颜色
color = ' '.join(etree_obj.xpath('//div[@id="choose-attr-1"]//i/text()'))
# 获取选择版本
edition = etree_obj.xpath('//div[@id="choose-attr-2"]//a/text()')
# 去除空格拼接成字符串
edition_src = ''
for ed in edition:
    edition_src += ed.strip() + ','
# 获取购买方式
buy = ''.join(etree_obj.xpath('//div[@id="choose-type"]//a/text()'))
# 获取套装
suit = ''.join(etree_obj.xpath('//div[@id="choose-suits"]//a/text()'))
# 获取增值保障
server = ''.join(etree_obj.xpath('//div[@id="choose-service"]//span/text()'))
# 去除空格拼接成字符串
server_src = ''
for s in server:
    server_src += s.strip()
# 获取白条分期
baitiao = ''.join(etree_obj.xpath('//div[@id="choose-baitiao"]//strong/text()'))
# 去除空格拼接成字符串
fenqi_src = ''
for b in baitiao:
    fenqi_src += b.strip()

# 把数据放在字典中
phone = {
    '京东价': price,
    '促销': promotion,
    '增值业务': vas,
    '重量': weight,
    '选择颜色': color,
    '选择版本': edition_src,
    '购买方式': buy,
    '套装': suit,
    '增值保障': server_src,
    '白条分期': fenqi_src
}
# 将数据转化为json格式
s = json.dumps(phone, ensure_ascii=False)
# 写入到本地
with open('phone.txt', 'w', encoding='utf-8') as fp:
    fp.write(s)
    print('保存成功')
