import random
import time

class Noise:
    collection = None
    logger = None
    active = True
    minimum = 34
    maximum = 204

    def __init__(self, collection, logger):
        self.collection = collection
        self.logger = logger

    def createNoise(self, location):
        if not self.active:
            return

        timekey = int(time.strftime("%H%M"))
        timekey = float(timekey)
        loc_min = self.minimum
        loc_max = self.maximum
        if location == 'Einsteins':
            loc_max = 50
        amount = random.randrange(loc_min, loc_max)
        current = int(round(time.time() * 1000))

        if timekey >= 2000: # 8pm
            timekey = timekey - 2000
            blank = 1 - (timekey / float(150))
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
