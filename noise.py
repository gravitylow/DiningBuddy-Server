import random
import time

class Noise:
    collection = None
    logger = None
    active = True
    minimum = 3
    maximum = 15

    def __init__(self, collection, logger):
        self.collection = collection
        self.logger = logger

    def createNoise(self, location):
        if not self.active:
            return
        
        amount = random.randrange(self.minimum, self.maximum)
        current = int(round(time.time() * 1000))
        for x in range(0, amount):
            name = "SERVER" + str(x) + location
            json = {"id":name, "lat":0, "lon":0, "location":location, "send_time":current, "time":current};
            key = {'id':name}
            self.collection.update(key, json, upsert=True) 
   
