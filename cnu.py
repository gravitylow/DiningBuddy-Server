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
from db import Database

scheduler = Scheduler()
scheduler.start()

client = Database.get_client()
db = client.cnu
feedback = db.feedback
feedback_archive = db.feedbackarchive
graphs = db.graphs
banned_users = db.banned_users

app = Flask(__name__)

# Data providers
locations = open(os.path.dirname(os.path.realpath(__file__)) + '/data/cnu.geojson','r').read().replace('\n', '')
alert_list = json_util.dumps(db.alerts.find())
info = Info(app, db)

def requeryInfo():
    info.createInfo()

scheduler.add_interval_job(requeryInfo, seconds = 60)
requeryInfo()

@app.route('/')
def index():
    abort(400)

"""
@apiDefine LocationNotFoundError
@apiVersion 1.0.0

@apiError LocationNotFound Data requested from non-existent location

@apiErrorExample Error-Response:
    HTTP/1.1 404 Not Found
    {
        "error": "Not Found"
    }
"""
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

"""
@apiDefine InvalidUpdateError
@apiVersion 1.0.0

@apiError InvalidUpdate Invalid, incomplete, or expired update sent

    HTTP/1.1 400 Bad Request
    {
        "error": "Bad request"
    }
"""
"""
@apiDefine InvalidFeedbackError
@apiVersion 1.0.0

@apiError InvalidFeedback Invalid, incomplete, or expired feedback sent

    HTTP/1.1 400 Bad Request
    {
        "error": "Bad request"
    }
"""
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

# Get

"""
@api {get} /error/ Force a server-side error
@apiName GetError
@apiGroup System
@apiVersion 1.0.0

@apiSuccess (500) error Internal Server Error
"""
@app.route('/cnu/api/v1.0/error/', methods = ['GET'])
def get_error():
    return json.dumps()

"""
@api {get} /alerts/ Request all active alerts
@apiName GetAlerts
@apiGroup System
@apiVersion 1.0.0

@apiSuccess {Object[]} alerts List of alerts
@apiSuccess {String} alerts.target_version Targeted DiningBuddy version
@apiSuccess {String} alerts.target_os Targeted host OS
@apiSuccess {String} alerts.target_time_min Targeted minimum system time
@apiSuccess {String} alerts.target_time_max Targeted maximum system time
@apiSuccess {Number} alerts.title Alert title
@apiSuccess {Number} alerts.title Alert message
@apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    [
        {
            "target_version": "1.0",
            "target_os": "iOS",
            "target_time_min": 1425248667519,
            "target_time_max": 1425248983741,
            "title": "Hello world!",
            "message": "What's up?"
        },
        {
            "target_version": "all",
            "target_os": "all",
            "target_time_min": 0,
            "target_time_max": 0,
            "title": "Heads up!",
            "message": "Everyone must know this."
        }
    ]
"""
@app.route('/cnu/api/v1.0/alerts/', methods=['GET'])
def get_alerts():
    return alert_list

"""
@api {get} /locations/ Request all locations
@apiName GetLocations
@apiGroup Location
@apiVersion 1.0.0

@apiSuccess {Object[]} locations GEOJson FeatureCollection of all locations
@apiSuccess {String} locations.type GEOJson location list format (always "FeatureCollection")
@apiSuccess {Object[]} locations.features GEOJson FeatureCollection
@apiSuccess {String} locations.features.type GEOJson location format (always "Feature")
@apiSuccess {Object[]} locations.features.properties GEOJson Feature properties
@apiSuccess {String} locations.features.properties.name Location name
@apiSuccess {Number} locations.features.properties.priority Location priority (higher number = more nested location)
@apiSuccess {Object[]} locations.features.style GEOJson Styling data
@apiSuccess {Object[]} locations.features.geometry GEOJson Geometry list
@apiSuccess {String} locations.features.geometry.type GEOJson Geometry format (always "Polygon")
@apiSuccess {Object[]} locations.features.geometry.coordinates GEOJson Coordinate list defining the polygon (lon, lat)
"""
@app.route('/cnu/api/v1.0/locations/', methods = ['GET'])
def get_locations():
    return locations

"""
@api {get} /info/ Request all location info
@apiName GetInfo
@apiGroup Location
@apiVersion 1.0.0

@apiSuccess {Object[]} info List of info
@apiSuccess {String} info.location Location name
@apiSuccess {Number} info.people People at the location
@apiSuccess {Number} info.crowded Crowded value of the location
@apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    [
        {
            "location": "Regattas",
            "crowded": 0,
            "people": 0
        },
        {
            "location": "Commons",
            "crowded": 0
            "people": 0
        },
        {
            "location": "Einsteins",
            "crowded": 0,
            "people": 0
        }
    ]
"""
@app.route('/cnu/api/v1.0/info/', methods = ['GET'])
def get_info():
    return json.dumps(info.getInfo())

"""
@api {get} /graphs/:location/ 24-hour user graph
@apiName GetGraph
@apiGroup Location
@apiVersion 1.0.0

@apiSuccess graph SVG of graph

@apiUse LocationNotFoundError
"""
@app.route('/cnu/api/v1.0/graphs/<location>/', methods=['GET'])
def get_graph(location):
    response = app.send_static_file('graphs/' + location + '.svg')
    response.mimetype = 'text/html'
    return response

"""
@api {get} /menus/:location/ Location's menu
@apiName GetMenu
@apiGroup Location
@apiVersion 1.0.0

@apiSuccess menu TXT of menu

@apiUse LocationNotFoundError
"""
#@app.route('/cnu/api/v1.0/menus/<location>', methods=['GET'])
#def get_menu_broken(location):
#    response = app.send_static_file('menus/' + location + '.txt')
#    return response

@app.route('/cnu/api/v1.0/menus/<location>/', methods=['GET'])
def get_menu(location):
    file = open(app.static_folder + '/menus/' + location + '.txt', 'r')
    #response = app.send_static_file('menus/' + location + '.txt')
    #response.mimetype = 'text/html'
    #return response
    return file.read()

"""
@api {get} /feed/:location/ Request location's feed
@apiName GetFeed
@apiGroup Location
@apiVersion 1.0.0

@apiSuccess {Object[]} feed List of feed items
@apiSuccess {String} feed.feedback Feedback message
@apiSuccess {Boolean} feed.pinned Feedback is pinned to the top
@apiSuccess {Number} feed.time Feedback Timestamp
@apiSuccess {Number} feed.minutes Minutes estimation
@apiSuccess {Number} feed.crowded Crowded estimation
@apiSuccess {String} feed.detail Detail message (may not exist)

@apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    [
        {
            "feedback": "The food is excellent",
            "pinned": false,
            "time": 1425248667519,
            "minutes": 1,
            "crowded": 1
        },
        {
            "feedback": "This is an important item",
            "pinned": true,
            "time": 1425248667519,
            "minutes": 1,
            "crowded": 1,
            "detail": "This is an important message"
        },
    ]

@apiUse LocationNotFoundError
"""
@app.route('/cnu/api/v1.0/feed/<location>/', methods=['GET'])
def get_feed(location):
    feed = feedback.find({'$or' : [{'target': location}, {'target': 'all'}], 'feedback':{"$exists" : True, "$ne" : "", "$ne": None}}).sort('time', pymongo.DESCENDING)
    if not feed:
        abort(404)
    return json_util.dumps(feed)

"""
@api {get} /info/:location/ Request specific location info
@apiName GetInfoLocation
@apiGroup Location
@apiVersion 1.0.0

@apiSuccess {String} location Location name
@apiSuccess {Number} people People at the location
@apiSuccess {Number} crowded Crowded value of the location
@apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
        "location": "Regattas",
        "crowded": 0,
        "people": 0
    }

@apiUse LocationNotFoundError
"""
@app.route('/cnu/api/v1.0/info/<location>/', methods = ['GET'])
def get_info_location(location):
    i = info.getInfoLocation(location)
    if i == 0:
        abort(404)
    else:
        return make_response(jsonify(i))

"""
@api {get} /maps/updates/ Update map
@apiName GetUpdateMap
@apiGroup Map
@apiVersion 1.0.0

@apiSuccess map Map page containing current updates
"""
@app.route('/cnu/api/v1.0/maps/updates/', methods=['GET'])
def get_map_updates():
    response = app.send_static_file('maps/updates.html')
    return response

# Post

"""
@api {post} /update/ Send update
@apiName SendUpdate
@apiGroup Location
@apiVersion 1.0.0
@apiHeader {String} User-Agent OS identifier.

@apiParam {String} id UUID
@apiParam {Number} lat Latitude
@apiParam {Number} lon Longitude
@apiParam {String} location Campus location
@apiParam {Number} send_time Timestamp

@apiParamExample {json} Request-Example:
    {
        "id": "123e4567-e89b-12d3-a456-426655440000",
        "lat": 37.06255308986635,
        "lon": -76.49493545293808,
        "location": "Regattas",
        "send_time": 1425248667519
    }
"""
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

"""
@api {post} /feedback/ Send Feedback
@apiName SendFeedback
@apiGroup Location
@apiVersion 1.0.0
@apiHeader {String} User-Agent OS identifier.

@apiParam {String} id UUID
@apiParam {String} target Targeted campus location
@apiParam {String} location Actual campus location
@apiParam {Number} crowded Crowded value
@apiParam {Number} minutes Minutes value
@apiParam {String} feedback Feedback message
@apiParam {Number} send_time Timestamp

@apiParamExample {json} Request-Example:
    {
        "id": "123e4567-e89b-12d3-a456-426655440000",
        "target": "Regattas",
        "location": "Regattas",
        "crowded": 1,
        "minutes": 1,
        "feedback": "Hello world!",
        "send_time": 1425248667519
    }
"""
@app.route('/cnu/api/v1.0/feedback/', methods = ['POST'])
def create_feedback():
    if not request.json or not 'id' in request.json:
        app.logger.warning(str(request.json) + ' disqualified for id')
        abort(400)
    
    key = {'id': request.json['id']}
    results = banned_users.find(key)
    app.logger.warning(str(key) + ': ' + str(results.count()))
    if results.count() > 0:
        app.logger.warning(str(request.json) + ' disqualified because they are banned')
        abort(400)
    current = int(round(time.time() * 1000))
    request.json['time'] = current

    if abs(current - request.json['send_time']) > 30 * 1000:
        app.logger.warning(str(request.json) + ' disqualified for time > ' + str(current))
        abort(400)

    request.json['pinned'] = False

    feedback.insert(request.json)
    feedback_archive.insert(request.json)
    return make_response("OK", 201)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', use_reloader=False)
