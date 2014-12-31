#!flask/bin/python
from pymongo import MongoClient
import time
import logging
from cnu import app
from noise import Noise

logger = app.logger;

max_time_update = 60 * 10 * 1000
max_time_feedback = 60 * 30 * 1000

client = MongoClient()
db = client.cnu
updates = db.updates
feedback = db.feedback
noise = Noise(db.updates, logger)

cursor = updates.find()
for record in cursor:
    updated = record.get('time')
    uuid = record.get('id')
    current = int(round(time.time() * 1000))
    if (current - updated) > max_time_update or uuid.startswith('SERVER'):
        updates.remove({"id": uuid})

for x in set(['Regattas', 'Commons', 'Einsteins']):
    noise.createNoise(x)
    logger.debug('created noise for ' + x)    
    print('created noise for ' + x)
cursor = feedback.find()
for record in cursor:
    updated = record.get('time')
    current = int(round(time.time() * 1000))
    if (current - updated > max_time_feedback) and not record.get('pinned'):
        id = record.get('id')
        feedback.remove({"id": id})
