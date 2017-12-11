# -*- coding: utf-8 -*-
import scrapy
import lxml
import string
import re
from time import mktime
from datetime import datetime, date
import parsedatetime

cal = parsedatetime.Calendar()



#from zawya.items import ZawyaItem

class ZawyaSpider(scrapy.Spider):
    name = "zawya1"
    allowed_domains = ["zawya.com"]
    start_urls = [
        "http://www.zawya.com/mena/en/press-releases/",
    ]
    url_base = 'http://www.zawya.com'
    emails_reg = re.compile(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+")


    # parse urls and extract links
    def parse(self, response):
        result = []
        for sel in response.xpath('//*[@id="items"]/article/div[@class="media-body"]'):
            article_url = sel.xpath('h3/a/@href').extract()
            article_title = sel.xpath('h3/a/text()').extract()
            article_pub_date = sel.xpath('span[@class="post-time"]/text()').extract()[0].strip()
            time_struct, parse_status = cal.parse(article_pub_date)
            article_pub_date = datetime(*time_struct[:6]).strftime("%Y-%m-%d")
            result.append({'url': self.url_base + str(article_url[0]), 'title': article_title[0], 'pub_date': article_pub_date})

            #code = entry[0]
            #url = self.url_base + code
            #yield scrapy.Request(url, lambda response, args=code: self.parse_dir_contents(response, args))
        yield {'crawler': 'zawya', 'articles': result}

        #printresult)
        #return None


    # parse link page
    def parse_dir_contents(self, response, code):
        item = ZawyaItem()
        info = response.xpath('//*[@id="main-content"]/div[1]/p[last() - 2]/child::node()').extract()

        if info:
            info = ' '.join(info).strip()
            info = self.clean_control_char(str(info))
            #emails = self.emails_reg.findall(info, re.I)
            #emails = list(set(emails))
            item = {'url': self.url_base + code, 'text': info}
            #item = {'url': self.url_base + code, 'emails': emails}

        yield item


    def clean_control_char(self, text):
        return text.translate(string.maketrans("\n\t\r", "   "))
