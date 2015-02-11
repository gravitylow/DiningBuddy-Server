#!flask/bin/python
from flask import Flask, jsonify, make_response, abort, request, Response, render_template
from pymongo import MongoClient
import pymongo
from bson import json_util
import json
import time
import random
import os
from apscheduler.scheduler import Scheduler
from info import Info

scheduler = Scheduler()
scheduler.start()

client = MongoClient()
db = client.cnu
feedback = db.feedback
feedback_archive = db.feedbackarchive
graphs = db.graphs

app = Flask(__name__)

# Data providers
locations = open(os.path.dirname(os.path.realpath(__file__)) + '/data/cnu.geojson','r').read().replace('\n', '')
alert_list = json_util.dumps(db.alerts.find())
info = Info(app, db)

def requeryInfo():
    info.createInfo()

def requeryAlerts():
    global alert_list
    alert_list = json_util.dumps(db.alerts.find())

scheduler.add_interval_job(requeryInfo, seconds = 60)
scheduler.add_interval_job(requeryAlerts, seconds = 60 * 5)

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
    return locations

@app.route('/cnu/api/v1.0/error/', methods = ['GET'])
def get_error():
    return json.dumps()

@app.route('/cnu/api/v1.0/info/', methods = ['GET'])
def get_info():
    return json.dumps(info.getInfo())

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

@app.route('/cnu/api/v1.0/info/<location>/', methods = ['GET'])
def get_info_location(location):
    i = info.getInfoLocation(location)
    if i == 0:
        abort(404)
    else:
        return make_response(jsonify(i))

@app.route('/cnu/api/v1.0/people/<location>/', methods = ['GET'])
def get_people(location):
    return make_response(str(info.getPeople(location)))

@app.route('/cnu/api/v1.0/crowded/<location>/', methods = ['GET'])
def get_crowded(location):
    return make_response(str(info.getCrowded(location)))

@app.route('/cnu/api/v1.0/maps/updates/', methods=['GET'])
def get_map_updates():
    response = app.send_static_file('maps/updates.html')
    return response
# Post

@app.route('/cnu/api/v1.0/update/', methods = ['POST'])
def update_user():
    if not request.json or not 'id' in request.json:
        app.logger.warning(str(request.json) + ' disqualified for id')
        abort(400)

    current = int(round(time.time() * 1000))
    request.json['time'] = current

    if abs(current - request.json['send_time']) > (120 * 1000):
        app.logger.warning(str(request.json) + ' disqualified for ' + str(current) + ' - ' + str(request.json['send_time']) + ' > 120 * 1000')
        app.logger.warning('Current time: ' + str(current))
        abort(400)

    key = {'id':request.json['id']}
    info.createUpdate(request.json, key)
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
