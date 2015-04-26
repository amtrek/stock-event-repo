import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Query import Query
from datetime import datetime
import datetime as dt
from pandas import DataFrame
import pandas.io.data as web
from pandas.tseries.offsets import BDay
from pandas import Series
from pandas.tseries.offsets import CustomBusinessDay
from pandas.tseries.holiday import USFederalHolidayCalendar
import sys, time


query = Query("localhost",27017,"stock")

hevent=query.set_collection("event")
fund = query.set_collection("fundamentals")

# Get split symobl within last two years 

data  = hevent.aggregate([
    {'$match':
        {"split.exdate":{'$gt': datetime(2012,1,1,0,0)}}},
    {'$unwind':"$split"},
    {'$match':{"split.exdate":{'$gt': datetime(2012,1,1,0,0)},"split.forwardSplit":True}}])



allevents = DataFrame(data[u'result'])
results = DataFrame()

indx = 0

for idx, event in allevents.iterrows():
    symbol = event[u'_id']
    exdate = event['split']['exdate']
    sys.stdout.flush()
    print '\r>> %d over %d is completed!' % ( idx, allevents.shape[0]),
    #sys.stdout.flush()
    if exdate.weekday() >= 6 or exdate > datetime.today():
        pass
    else:
        start =  exdate

        bday_us = CustomBusinessDay(calendar=USFederalHolidayCalendar())        
        delta = 180
        end = start + BDay(delta)
        if end > datetime.today():
            continue
        
        #print symbol
        complete = False
        try:
        
            trial = 0
            while not complete: 

                out =web.DataReader(symbol, 'yahoo', start, end)
                s  = [s for i in range(0,5) s = out.ix[start+BDay(i*30)]]
                prices = [p for si in s p = s['Adj Close'] ]
                if trial>5 :
                    raise DataRetrivalError('HiThere')

                elif out1.shape[0] == 0 or out2.shape[0] == 0 or out3.shape[0]==0:
                
                    raise DataRetrivalError("Error")
                else:
                    complete = True
                trial+=1

            split_day = out['Adj Close'][0]
        
         #Return is a series
            returns = (split_day - out["Adj Close"].shift(1))
            returns = returns.tolist()
            returns.insert(0,symbol)
            s = Series(data = returns, index = ['symbol','Return'], name = indx)
            
            results = results.append(s)
            
            indx +=1

            #print out
        except :
            print "Unexpected error:", sys.exc_info()[0]
        
        
