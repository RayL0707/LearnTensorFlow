# -*- coding: utf-8 -*-
from lxml import etree
from SinaSpider.items import SinaspiderItem
response = etree.parse('./2018-01-26.html', etree.HTMLParser())
# result = etree.tostring(html)

# articals = html.xpath('//ul[@class="list01"]//li//a')

# for artical in articals:
# 	print(artical.text)
# 	print(artical.xpath('@href')[0])
item = SinaspiderItem()
item['title'] = response.xpath('//h1[@class="main-title"]')[0].text
basicINFO = response.xpath('//div[@class="top-bar-wrap"]//div[@id="top_bar"]//div[@class="date-source"]')[0]
item['source'] = basicINFO.xpath('//span[@class="source ent-source"]')[0].text
item['date'] = basicINFO.xpath('//span[@class="date"]')[0].text
texts = response.xpath('//div[@id="artibody"]/p')
item['content'] = text + '\n' for text in texts
keywords = response.xpath('//div[@id="article-bottom"]//div[@class="keywords"]//a')
item['keywords'] = [key.text for key in keywords]

