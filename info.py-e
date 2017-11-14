class Info:
    collection = None
    ban_collection = None
    cursor = None
    logger = None
    info = []

    def __init__(self, app, db):
        self.logger = app.logger
        self.collection = db.updates
        self.ban_collection = db.banned_users
        self.cursor = self.collection.find()
        self.createInfo()

    def createInfo(self):
        self.cursor = self.collection.find()
        self.info = []

        # Insert necessary info
        self.info.append({'location':'Regattas','people':0,'crowded':0})
        self.info.append({'location':'Commons','people':0,'crowded':0})
        self.info.append({'location':'Einsteins','people':0,'crowded':0})
        
        # Parse current updates
        for record in self.cursor:
            location = record.get('location')
            found = False
            for i in self.info:
                if i.get('location') == location:
                    found = True
                    people = i.get('people')+1
                    crowded = 2 if people > 150 else 1 if people > 100 else 0
                    i.update({'people':people})
                    i.update({'crowded':crowded})
                    break

        return self.info

    def createUpdate(self, json, key):
        results = self.ban_collection.find(key)
        if results.count() is 0:
        	self.collection.update(key, json, upsert=True)

    def getInfo(self):
        return self.info

    def getInfoLocation(self, location):
        for x in self.info:
            if x['location'] == location:
                return x
        return 0

    def getPeople(self, location):
        for x in self.info:
            if x['location'] == location:
                return x['people']
        return 0

    def getCrowded(self, location):
        for x in self.info:
            if x['location'] == location:
                return x['crowded']
        return 0
