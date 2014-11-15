#!flask/bin/python
from pymongo import MongoClient
import time

max_time_update = 60 * 2 * 1000
max_time_feedback = 60 * 30 * 1000

client = MongoClient()
db = client.cnu
updates = db.updates
feedback = db.feedback

cursor = updates.find()
for record in cursor:
    updated = record.get('time')
    current = int(round(time.time() * 1000))
    if current - updated > max_time_update:
        id = record.get('id')
        updates.remove({"id": id})

cursor = feedback.find()
for record in cursor:
    updated = record.get('time')
    current = int(round(time.time() * 1000))
    if (current - updated > max_time_feedback) and not record.get('pinned'):
        id = record.get('id')
        feedback.remove({"id": id})
