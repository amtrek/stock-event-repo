# -*- coding: utf-8 -*-
"""
This spider scrawl splitting data from yahoo finance dividend & 

"""
import scrapy
import pymongo
from scrapy.conf import settings
from scrapy import log
from stock.items import SplitEvent
from datetime import datetime

class YahooSpider(scrapy.Spider):
    name = "yahoo"
    allowed_domains = ["finance.yahoo.com"]

    def __init__ (self):
        connection = pymongo.Connection(
                
                settings['MONGODB_SERVER'],
                settings['MONGODB_PORT']
                )
        #select database
        db = connection[settings['MONGODB_DB']]
        self.collection_basic = db[settings['MONGODB_COLLECTION_BASIC']]
        symbols = self.collection_basic.distinct('Symbol')
        self.baseurl = 'http://finance.yahoo.com/q/hp?s='
        begin_yr = "2012"
        end_yr = "2016"
        self.restricturl = '&a=1&b=1&c='+begin_yr+'&d=1&e=1&f='+end_yr+'&g=v&z=66&y=0'
        self.start_urls = [self.baseurl+symbol+self.restricturl for symbol in symbols]
        #self.start_urls = [self.baseurl+"SBUX"+self.restricturl]
        
    def parse(self, response):
         
        #check split stock exist 
        has_split =  "Stock Split"

        if has_split in response.body:

            symbol = response.url.strip(self.baseurl).strip(self.restricturl) 
            split_ratios=response.xpath("//tr/td[contains(.//text(), 'Stock Split')]/text()").extract()
            exdates=response.xpath("//tr/td[contains(.//text(), 'Stock Split')]/preceding-sibling::td/text()").extract()

            
            for split_ratio,exdate in map (None,split_ratios,exdates):
                
                item = SplitEvent()
                ratio, forward_split = self.get_ratio(split_ratio)
                exdate, executed = self.get_exdate(exdate)
                print ratio, forward_split
                #Store Event Data
                item['symbol'] = symbol
                item['ratio'] = ratio
                item['exdate'] = exdate
                item['executed'] = executed
                item['event']='split'
                item['forwardSplit'] = forward_split
                yield item

        pass


    def get_ratio(self, split_ratio):

       split_ratio=split_ratio.encode('utf-8').replace('Stock Split','').replace(" ",'').replace('\n','')
       split_ratio = split_ratio.split(':')
       ratio = float(split_ratio[0])/float(split_ratio[1])
        

       if ratio > 1:
           forward_split = True
       else:
           forward_split = False
      
       
       return (ratio, forward_split)

    def get_exdate(self, exdate):

        exdate = datetime.strptime(exdate.encode('utf-8'), '%b %d, %Y')

        if exdate > datetime.today():
            executed = False
        else:
            executed = True

        return (exdate, executed)



