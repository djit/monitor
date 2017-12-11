import pymongo
from datetime import datetime
from bson.objectid import ObjectId


def set_pub_date_short:
    articles = db.articles.find()
    return articles