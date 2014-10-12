#!/usr/bin/env python
from pymongo import MongoClient
import time

max_time = 60 * 2 * 1000

client = MongoClient()
db = client.cnu
updates = db.updates

cursor = updates.find()
for record in cursor:
    updated = record.get('time')
    current = int(round(time.time() * 1000))
    if current - updated > max_time:
        id = record.get('id')
        updates.remove({"id": id})
