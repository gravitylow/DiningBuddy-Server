#!flask/bin/python
from flask import Flask, jsonify, make_response, abort, request, Response
from pymongo import MongoClient
import pymongo
from bson import json_util
import json
import time
import random
import os
from apscheduler.scheduler import Scheduler

scheduler = Scheduler()
scheduler.start()

client = MongoClient()
db = client.cnu
updates = db.updates
feedback = db.feedback
feedback_archive = db.feedbackarchive
graphs = db.graphs
info = []

update_cursor = updates.find()
alert_list = json_util.dumps(db.alerts.find())

location_list = location_list = list(db.locations.find())

locations = open(os.path.dirname(os.path.realpath(__file__)) + '/data/cnu.geojson','r').read().replace('\n', '')

app = Flask(__name__)

def requery_updates():
    app.logger.debug('Requerying updates!')
    global update_cursor
    update_cursor = updates.find()

    global info
    info = []
    for record in update_cursor:
        location = record.get('location')
        found = False
        for i in info:
            if i.get('location') == location:
                found = True
                people = i.get('people')
                i.update({'people':people+1})
        if not found:
            info.append({'location':location,'people':1})
    hasR = False
    hasC = False
    hasE = False
    for i in info:
        if i.get('location') == 'Regattas':
            hasR = True
        if i.get('location') == 'Commons':
            hasC = True
        if i.get('location') == 'Einsteins':
            hasE = True
        people = i.get('people')
        people = people + random.randrange(3,15)
        crowded = 1 if people > 20 else 2 if people > 50 else 0
        i.update({'crowded':crowded})
    if not hasR:
        info.append({'location':'Regattas','people':random.randrange(3,15),'crowded':0})
    if not hasC:
        info.append({'location':'Commons','people':random.randrange(3,15),'crowded':0})
    if not hasE:
        info.append({'location':'Einsteins','people':random.randrange(3,15),'crowded':0})

scheduler.add_interval_job(requery_updates, seconds = 60)

@app.route('/')
def index():
    abort(400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

# Get

@app.route('/cnu/api/v1.0/locations/', methods = ['GET'])
def get_locations():
    return json.dumps(location_list, default=json_util.default)

@app.route('/cnu/api/v1.0/locations2/', methods = ['GET'])
def get_locations2():
    return locations

@app.route('/cnu/api/v1.0/error/', methods = ['GET'])
def get_error():
    return json.dumps()

@app.route('/cnu/api/v1.0/info/', methods = ['GET'])
def get_info():
    return json.dumps(info)

@app.route('/cnu/api/v1.0/alerts/', methods=['GET'])
def get_alerts():
    return alert_list

@app.route('/cnu/api/v1.0/graphs/<location>/', methods=['GET'])
def get_graph(location):
    response = app.send_static_file('graphs/' + location + '.svg')
    response.mimetype = 'text/html'
    return response

@app.route('/cnu/api/v1.0/menus/<location>/', methods=['GET'])
def get_menu(location):
    response = app.send_static_file('menus/' + location + '.txt')
    return response

@app.route('/cnu/api/v1.0/feed/<location>/', methods=['GET'])
def get_feed(location):
    feed = feedback.find({'target': location, 'feedback':{"$exists" : True, "$ne" : "", "$ne": None}}).sort('time', pymongo.DESCENDING)
    if not feed:
        abort(404)
    return json_util.dumps(feed)

# Post

@app.route('/cnu/api/v1.0/update/', methods = ['POST'])
def update_user():
    if not request.json or not 'id' in request.json:
        abort(400)

    current = int(round(time.time() * 1000))
    request.json['time'] = current

    if abs(current - request.json['send_time']) > 30 * 1000:
        abort(400)

    key = {'id':request.json['id']}
    updates.update(key, request.json, upsert=True)
    return make_response("OK", 201)

@app.route('/cnu/api/v1.0/feedback/', methods = ['POST'])
def create_feedback():
    if not request.json or not 'id' in request.json:
        abort(400)

    current = int(round(time.time() * 1000))
    request.json['time'] = current

    if abs(current - request.json['send_time']) > 30 * 1000:
        abort(400)

    request.json['pinned'] = False

    feedback.insert(request.json)
    feedback_archive.insert(request.json)
    return make_response("OK", 201)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', use_reloader=False)
