# -*- coding: utf-8 -*-
import scrapy
import lxml
import string
import re
from time import mktime
from datetime import datetime, date
import parsedatetime
from bs4 import BeautifulSoup
import logging
import sys
sys.path.append(APP_DIR)
sys.path.append("/var/www/monitor")
from app import app, db
from app.lib.utils.logger import mongoLogger

# calendar for relative date/time handling
cal = parsedatetime.Calendar()

#logs handler


class ZawyaSpider(scrapy.Spider):
    name = "zawya2"
    domain = "zawya.com"
    allowed_domains = ["zawya.com"]
    start_urls = [
        "http://www.zawya.com/mena/en/press-releases/",
    ]
    url_base = 'http://www.zawya.com'
    emails_reg = re.compile(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+")

    mongolog = mongoLogger(db)

    # logging & counter
    i = 0
    mongolog.add("- starting crawler " + name + " for " + url_base)

    # parse urls and extract links
    def parse(self, response):
        for sel in response.xpath('//*[@id="items"]/article/div[@class="media-body"]'):
            self.i += 1
            article_url = sel.xpath('h3/a/@href').extract()
            article_url = self.url_base + str(article_url[0])
            article_title = sel.xpath('h3/a/text()').extract()
            article_pub_date = sel.xpath('span[@class="post-time"]/text()').extract()[0].strip()
            time_struct, parse_status = cal.parse(article_pub_date)
            #article_pub_date = datetime(*time_struct[:6]).strftime("%Y-%m-%d")
            article_pub_date = datetime(*time_struct[:6])
            article_meta = {
                'url': article_url,
                'title': article_title[0],
                'pub_date': article_pub_date,
                'pub_date_short': article_pub_date.date(),
                'source': self.domain
            }

            yield scrapy.Request(article_url, lambda response, args=article_meta: self.parse_article(response, args))

        #logging.info("- " +  str(self.i) + " articles parsed")
        self.mongolog.add("- " + str(self.i) + " articles parsed")
        self.mongolog.store()

    # parse link page
    def parse_article(self, response, article_meta):
        article_body = response.xpath('//div[@class="articleContent"]/node()').extract()
        article_body = '\n'.join(filter(None, article_body))
        article_body = self.cleanHtml(article_body)
        article = {
            'url': article_meta['url'],
            'title': article_meta['title'],
            'pub_date': article_meta['pub_date'],
            'source': article_meta['source'],
            'body': article_body,
            'mongolog': self.mongolog
        }
        yield article


    # clean text from unwanted html tags
    def cleanHtml(self, html):
        blacklist = ["script", "style"]
        whitelist = ["br"]
        plist = ["p"]

        soup = BeautifulSoup(html, 'lxml') # create a new bs4 object from the html data loaded
        for tag in soup.findAll():
            if tag.name.lower() in blacklist:
                tag.extract()
            elif tag.name.lower() in whitelist:
                tag.replace_with('\n')

        # get cleanedup html
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n\n'.join(chunk for chunk in chunks if chunk)
        return text
