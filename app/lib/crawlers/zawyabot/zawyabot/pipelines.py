# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from datetime import datetime
from scrapy.mail import MailSender
#import logging
import sys
sys.path.append("/Users/dji/Dropbox/workspace/code/alpcontentservices/monitor")
sys.path.append("/var/www/monitor")
from app import app, db
from app.lib.utils import mailer
from app.lib.utils.logger import mongoLogger


class MongoDBPipeline(object):

    collection_name = 'articles'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = app.config['DB_SERVER'],
            mongo_db = app.config['DB_NAME'],
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    # process item
    def process_item(self, item, spider):
        try:
            article = self.db[self.collection_name].find_one({'url': item['url']})
            mongolog = item['mongolog']
            if article is None:
                print('new article:', item['title'])
                item['last_run_time'] = datetime.now()
                item['status'] = 'new'
                del (item['mongolog'])
                result = self.db[self.collection_name].replace_one({'url': item['url']}, dict(item), upsert=True)
                if result.upserted_id:
                    mongolog.add("- new article: " + item['title'])
                    params={'url': item['url'], 'title': item['title'], 'article': app.config['SERVER_URL'] + '/admin/articles/' + str(result.upserted_id)}
                    self.notify_email(params)
        except Exception as e:
            mongolog.add(' -ERROR:',  e)
        finally:
            return item


    # send mail
    def notify_email(self, params):
        mailer.send_email({
            'from': 'no-reply@alpcontentservices.com',
            'to': "dtabbouche@gmail.com",
            'subject': "New article: " + str(params['title']),
            'body': "New aticle: <a href=" + params['article'] + ">" + str(params['title']) + "</a>"
            }
        )
