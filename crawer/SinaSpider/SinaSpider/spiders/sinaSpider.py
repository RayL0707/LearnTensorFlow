# -*- coding: utf-8 -*-
#spider for sina finance
import scrapy
from SinaSpider.items import SinaspiderItem
from lxml import etree
try:
    from urllib.parse import unquote
except ImportError:
     from urlparse import unquote

class sinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['finance.sina.com.cn']
    start_urls = ('http://finance.sina.com.cn/stock/', )
    #start_urls = ('http://finance.sina.com.cn/stock/jsy/2018-01-26/doc-ifyqyuhy6674973.shtml', )

    def parse(self, response):
        filename = response.url.split('/')[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
            html = etree.HTML(response.body)
            #print(html)
            articals = html.xpath('//ul[@class="list01"]//li//a')
            try:
                cnt = 1
                for artical in articals:
                    # if cnt > 2:
                    #     break
                    #print("get artical: %d" %cnt)
                    subURL = artical.xpath('@href')[0]
                    #print("sub", subURL)
                    cnt += 1
                    # dig into each artical page
                    yield scrapy.Request(subURL, callback = self.parse_post)
            except Exception:
                print("ERROR\n")


    def parse_post(self, response):
        item = SinaspiderItem()
        cur_url = unquote(response.url)
        try:
            item['url'] = cur_url
            html = etree.HTML(response.body)
            #print(html)
            item['title'] = html.xpath('//h1[@class="main-title"]')[0].text
            basicINFO = html.xpath('//div[@class="top-bar-wrap"]//div[@id="top_bar"]//div[@class="date-source"]')[0]
            item['source'] = basicINFO.xpath('//span[@class="source ent-source"]')[0].text
            item['date'] = basicINFO.xpath('//span[@class="date"]')[0].text
            item['content'] = html.xpath('//div[@id="artibody"]/p')[0].text
            keywords = html.xpath('//div[@id="article-bottom"]//div[@class="keywords"]//a')
            item['keywords'] = [key.text for key in keywords]
            print("processing url: %s" %cur_url)
            yield item
        except Exception as e:
            filename = 'error_links.txt'
            with open(filename, 'a') as f:
                f.write(cur_url +'\n')
            #print(str(e))
            #print(unquote(response.url))
            return
        pass
