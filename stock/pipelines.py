# -*- coding: utf-8 -*-

import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

class StockPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoDBPipeline(object):
    
    def __init__(self):
        connection = pymongo.Connection(
                settings['MONGODB_SERVER'],
                settings['MONGODB_PORT']
                )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
     
    def process_item(self, item, spider):
        
        #If data exist: skip else, add or update
        self.spider = spider
        data = dict(item)
        symbol = data.pop('symbol',None)
        event  = data.pop('event',None)


        if  self.collection.find({'_id':symbol}).count()==0:
            
            self.addEvent(symbol,event,data)
        else:
            self.updateEvent(symbol,event,date)
        
        return item


    
    def addEvent(self,symbol,event,data):
        
        self.collection.insert({'_id': symbol,'split':[data]})
        log.msg('Insert stock symbol '+symbol+'with Event '+event,level = log.DEBUG, spider = self.spider)

    def updateEvent(self,symbol,event,data):
        
        self.collection.update({'_id':symbol},{'$addToSet':{'split': data}})
        log.msg('Update stock symbol '+symbol+'with Event '+event,level = log.DEBUG, spider = self.spider)
