import pymongo
from datetime import datetime
from bson.objectid import ObjectId

class mongoLogger:


    def __init__(self, db):
        self.db = db
        self.msgbuffer = []

    # write new log entry
    # return log document id
    def start(self, msg):
        data = {}
        data['msg'] = [msg]
        data['timestamp'] = datetime.now()
        result = self.db['logs'].insert_one(data)
        return str(result.inserted_id)

    # update log entry with new message
    def store0(self, id, msg):
        print('updating log', id)
        self.db['logs'].update({'_id': ObjectId(id)}, {'$addToSet': {'msg': msg}})


    def add(self, msg):
        self.msgbuffer.append(msg)


    def store(self):
        data ={'timestamp': datetime.now(), 'msg': self.msgbuffer}
        self.db['logs'].insert_one(data)
        self.msgbuffer = []
