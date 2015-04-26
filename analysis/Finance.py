from datetime import datetime
import datetime as dt
import pandas as pd
from pandas.tseries.offsets import BDay # business day
from pandas import DataFrame
from pandas import Series
import pandas.io.data as web
from pandas.tseries.holiday import USFederalHolidayCalendar 
from pandas.tseries.offsets import CustomBusinessDay
 
   

def get_quote (source = 'yahoo', symbol ='AAPL', \
        start = datetime(2014,1,16,0,0), end = None, freq = None):

    error = False
    start, adjusted = validate(start)

    if not end:
        end = start

    if end < start:
        raise ValueError("end date is eariler then start date")
    


    if freq:
        # quote periodically
        quote, error = quote_periodic(source, symbol,start,end,freq)
    
    else:
        # if end date exist, quote a range, else quote a date
        print "quoting " + symbol + "@ date:" + start.__str__() + "to date: "+ end.__str__()
        quote, error = quote_date(source, symbol, start, end)

    return quote, error 

def quote_periodic (source = 'yahoo', symbol = 'AAPL', \
                    start = datetime(2014,1,16,0,0), end=datetime(2015,1,16,0,0), freq = 1 ):
   
    print "Quoting periodic data..."

    error = False
    date = start
    quotes = DataFrame()
    #Periodic Retrival
    while date < end or date > datetime.today():
        
        date, adjusted = validate(date)
        quote, error = quote_date(source, symbol, date )
        date += BDay(freq)
        print quote
        quotes = quotes.append(quote)
    return quotes, error


def quote_date (source = 'yahoo', symbol = 'AAPL',start = datetime(2014,1,16,0,0), end = None):

    print "Quoting data..."
    start, adjusted = validate(start)
    error = False

    if not end:
        end = start # when end date is not given, quote on a specific day, otherwise quote a range
    try:
        end, adjusted = validate(end)
        quote = web.DataReader(symbol, source, start, end)
    except:
        print "Exception!"
        error = True
        quote = DataFrame()    

    return quote, error


def validate ( date ):
  
    cal = USFederalHolidayCalendar() 
    holidays = cal.holidays(date) # check recent holidays

    adjusted = False

    if date in holidays:
        #create offset, where offset replace BDay as bussiness day offset to account for holiday
        offset = CustomBusinessDay(calendar=cal)
        date+=offset
        adjusted = True

    return date, adjusted





