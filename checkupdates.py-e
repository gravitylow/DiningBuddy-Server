#!flask/bin/python
from bson.json_util import loads, dumps
from pymongo import MongoClient
import pymongo
from time import strftime
import pygal
from pygal import Config
from pygal.style import LightSolarizedStyle, LightGreenStyle
import random
client = MongoClient()
db = client.cnu

locations = ['Regattas','Commons','Einsteins']
updates = db.updates
cursor = db.updates.find()
graphs = db.graphs
time = strftime("%H:%M")
displayTime = strftime("%I:%M%P")
timeKey = int(strftime("%H%M"))
info = []

for location in locations:
    info.append({'location':location,'people':0})

# Generate Map
js = "var map = L.map('map').setView([37.063130980486, -76.49447679519653], 17);L.tileLayer('https://{s}.tiles.mapbox.com/v3/{id}/{z}/{x}/{y}.png', {maxZoom: 18,id: 'examples.map-i875mjb7'}).addTo(map);"
for record in cursor:
    uuid = record.get('id')
    location = record.get('location')
    lat = record.get('lat')
    lon = record.get('lon')
    print (uuid)
    print (location)
    print (lat)
    print (lon)
    js = js + "L.marker([" + str(lat) + "," + str(lon) + "]).addTo(map).bindPopup(\"<b>Location:</b> " + location + "<br /><b>UUID:</b> " + uuid + "\");"

jsfile = open('/var/www/api.gravitydevelopment.net/cnu/static/maps/updates.js', 'w')
jsfile.write(js)

cursor = db.updates.find()

# Sum people
for record in cursor:
    location = record.get('location')
    for i in info:
        if i.get('location') == location:
            people = i.get('people')
            i.update({'people':people+1})

for location in locations:
    people = 0
    for i in info:
        if i.get('location') == location:
            people = i.get('people')
    insert = {'id':time + "_" + location, 'key':timeKey, 'time':time, 'displayTime':displayTime, 'location':location, 'people':people}
    key = {'id':time + "_" + location}
    graphs.update(key, insert, upsert=True)

    # Generate graph

    graph = graphs.find({'location': location}).sort("key", pymongo.ASCENDING)
    obj = loads(dumps(graph))

    config = Config()
    config.show_legend = False
    config.fill = True
    config.style = LightGreenStyle
    config.x_label_rotation = 80
    config.show_only_major_dots = True
    config.x_labels_major_every = 2
    config.show_minor_x_labels = False
    config.show_minor_y_labels = False
    config.major_label_font_size = 12
    config.print_values = False
    config.print_zeroes = True
    config.disable_xml_declaration = True
    chart = pygal.Line(config)

    t = []
    p = []
    for l in obj:
        tt = l.get('displayTime')
        if tt.startswith('0'):
            tt = tt[1:]
        t.append(tt)
        p.append(int(l.get('people')))
    chart.x_labels = t
    chart.add('People', p)
    chart.render_to_file('/var/www/api.gravitydevelopment.net/cnu/static/graphs/' + location + '.svg')
