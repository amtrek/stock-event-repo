import csv
import glob
import json
import pymongo
from pymongo import MongoClient
files = glob.glob('*.csv')

print files

#jsonfile = 'symbols.json'


connection = pymongo.Connection('localhost',27017)
db = connection['stock']
collection = db['fundmental']


data = []

for file in files:    

    with open(file,'rb') as csvfile:

        stockreader = csv.DictReader(csvfile)
    
        for row in stockreader:
            #print type(row) 
            row.pop('', '')
            row.pop('LastSale', '')

            if row['MarketCap'][-1] == 'M':
                row['MarketCap'] = row['MarketCap'].strip('M').strip('$')
            
            elif row['MarketCap'][-1] == 'B':

                cap = float( row['MarketCap'].strip('B').strip('$') ) 
                row['MarketCap'] = str( cap * 1000 )

            if collection.find( {'Symbol' : row['Symbol']} ).count() == 0:
                collection.insert(row)
                #print "Log Data"

            
            #data.append(row)


