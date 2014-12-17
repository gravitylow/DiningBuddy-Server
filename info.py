class Info:
    collection = None
    cursor = None
    logger = None
    info = []

    def __init__(self, app, db):
      self.logger = app.logger
      logger.debug('created new info')
      self.collection = db.updates
      self.cursor = collection.find()

   def createInfo(self):
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
                 crowded = 1 if people > 20 else 2 if people > 50 else 0
                 i.update({'people':people})
                 i.update({'crowded':crowded})
         if not found:
             self.info.append({'location':location,'people':1,'crowded':0})

    return self.info

   def getInfo(self):
      return self.info
