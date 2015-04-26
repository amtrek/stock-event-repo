# -*- coding: utf-8 -*-
import scrapy
import pymongo 
from scrapy.conf import settings
from scrapy import log
from scrapy.exceptions import DropItem
from stock.items import SplitEvent
from datetime import datetime




class SplithistorySpider(scrapy.Spider):
    name = "splithistory"
    allowed_domains = ["getsplithistory.com"]
    
    def __init__(self):
        connection = pymongo.Connection(
                settings['MONGODB_SERVER'],
                settings['MONGODB_PORT']
                )
        #Fundamental Database to Retrive All US Stock
        db = connection[settings['MONGODB_DB']] 
        self.collection_basic = db[settings['MONGODB_COLLECTION_BASIC']]
        #self.collection_event = db[settings['MONGODB_COLLECTION_EVENT']]
        symbols = self.collection_basic.distinct('Symbol')
        baseurl = 'http://www.getsplithistory.com/'
        self.start_urls = [baseurl+symbol.encode('utf-8') for symbol in symbols ]


    def parse(self, response):
        log.msg('scrapying '+response.url)
        
        check = response.xpath(
                '//div[@class="splits-text"]/text()').extract()
        norecord = "as had no splits since its stock began trading publicly."
        
        if norecord not in check:
            
            symbol = response.url.split('/')[-1]
            ratios = self.get_ratio(response)
            exdates = self.get_exdate(response)
            
            for ratio, exdate in map ( None,ratios, exdates ):
                item = SplitEvent()
                item['symbol'] = symbol
                item['ratio'] = ratio
                item['exdate'] = exdate
                item['event'] = 'split'

                if ratio > 1 :
                    item['forwardSplit'] = True
                else:
                    item['forwardSplit'] = False
                
                if exdate > datetime.today():
                    item['executed'] = False
                else:
                    item['executed'] = True
                
                yield item

        pass
    
    def get_ratio(self, response):
        
        ratio1 = response.xpath('//tbody/tr/td[@class="bold"]/text()').extract()
        ratio1 = [ float(base.encode('utf-8').strip(' : ')) for base in ratio1]
        
        ratio2 = response.xpath('//tbody/tr/td[@class="bold"]/span/text()').extract()
        ratio2 = [ float(base.encode('utf-8')) for base in ratio2]
        
        ratio = []

        for r1,r2 in map(None, ratio1, ratio2):
            ratio.append(r2/r1)
        
        return ratio

    def get_exdate(self, response):
        
        data = response.xpath('//tbody/tr/td/text()').extract()
        
        dates = data[0::4]
        dates = [date.encode('utf-8') for date in dates if date.encode('utf-8') != "\xc2\xa0"]
        exdates = []
        
        for date in dates:
            exdates.append( datetime.strptime(date,'%b %d, %Y'))

        return exdates
