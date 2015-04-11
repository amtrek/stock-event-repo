# -*- coding: utf-8 -*-
import scrapy
from stock.items import SplitEvent
import re
from datetime import datetime


class NasdaqSpider(scrapy.Spider):
    name = "nasdaq"
    allowed_domains = ["nasdaq.com"]
    start_urls = (
        'http://www.nasdaq.com/markets/upcoming-splits.aspx',
    )

    def parse(self, response):
        Item = [];
        hrefs =  response.xpath('//td[@class="th_No_BG"]/a/@href').extract()
        
        split_detail = response.xpath('//tr/td/text()').extract()
        split_detail = [detail.replace(u'\xa0','N/A') for detail in split_detail if not "\n" in detail]
        split_detail = self.groups(split_detail,4)
        print split_detail 
        for href, detail in map(None,hrefs,split_detail):
          item = SplitEvent()
          item['symbol'] = href.split('/')[-1].encode('utf-8')
          item['ratio'] = self.parse_ratio(detail[0])
          item['exdate'] = datetime.strptime(detail[2].encode('utf-8'), '%m/%d/%Y')
          
          if(item['ratio']>1):
            item['forwardSplit'] = True
          else:
            item['forwardSplit'] = False

          if(item['exdate']>datetime.today()):
            item['executed'] = True
          else:
            item['executed'] = False
          
          yield item

          

    #Group 4 items into turple with 
    
    def groups(self, lst, n):
        
        return [lst[i:i+n] for i in range(0,len(lst)-n+1,n)]
       
    def parse_ratio(self,ratio):
        
        out = re.findall('\d+', ratio)
        
        if ratio[-1]!='%':
          return int(out[0])/int(out[1]) 
        else:
          try:
            return float(out[0])/100
          except:
            return float(0)
         

