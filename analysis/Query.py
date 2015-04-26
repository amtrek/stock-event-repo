import pymongo

from datetime import datetime






class Query ():

    def __init__(self, host, port, db):
        
        print "Building Connection....."
        self.host = host
        self.port = port
        self.valid_connection = False
        
        try:
            connection = pymongo.Connection(host, port)
            self.db = connection[db]
            print "Connection is built !"
            self.valid_connection = True
        except:
            print "Failed to build connection..!"
    
    def reconnecton(self, host="localhost", port=27017, db="test"):
        print "Building Connection at " + host +'/'+port 
         
        try:
            connection = pymongo.Connection(self.host, self.port)
            self.db = connection[db]
            self.host = host
            self.port = port
            self.collection = None

            print "Connection is build!"

            self.valid_connection = True
            return self.valid_connection

        except "ConnectionInvalid":

            print "Failed to build connection"
            self.valid_connection = False
            return self.valid_connection
            

    def set_collection(self, collection):
        #Use specific collection
        if not self.valid_connection:
            print "Invalid Connection ! Try Query.reconnection()!"
            
        else:
            self.collection = self.db[collection]
            print "currently using collection " + collection
            return self.collection

    def get_collection(self):
        #get current collection
        print self.collection.__str__()

    def get_collection_all(self):
        #return all collrection as list

        pass
    
    #Query price with a symbol but mutiple dates specified
    def get_price(self, symbols, dates):
        
        if self.valid_connection:
            for symbol, date in map(None,symbols,dates):
                yield yahoofinance(symbol,'price','date',date)
    



    #Filter Market Cap / Split Event Year / Stock Price(?) 
    def filter(self, db_handler, args, criteria):
        
        if args =='MktCap':
            data = self.collection.find({'Market Cap'})        
        elif args == 'Price':
            pass
    
  
 
    
