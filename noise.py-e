import random
import time

class Noise:
    collection = None
    logger = None
    active = True
    minimum = 7
    maximum = 15

    def __init__(self, collection, logger):
        self.collection = collection
        self.logger = logger

    def createNoise(self, location):
        if not self.active:
            return
        
        timekey = int(time.strftime("%H%M"))
        timekey = float(timekey)
        amount = random.randrange(self.minimum, self.maximum)
        
        if timekey >= 2000: # 8pm
            timekey = timekey - 2000
            blank = 1 - (timekey / float(300))
            amount = int(round(amount * blank))
            if amount < 0:
                amount = 0
        elif timekey < 900: # 10am
            timekey = timekey - 700
            if timekey < 0:
                amount = 0
            else:
                blank = (timekey / float(200))
                amount =  int(round(amount * blank))
        
        for x in range(0, amount):
            name = "SERVER" + str(x) + location
            json = {"id":name, "lat":0, "lon":0, "location":location, "send_time":current, "time":current};
            key = {'id':name}
            self.collection.update(key, json, upsert=True) 
   
