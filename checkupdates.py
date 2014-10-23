#!/usr/bin/env python
from bson.json_util import loads, dumps
from pymongo import MongoClient
import pymongo
from time import strftime
import pygal
from pygal import Config
from pygal.style import LightSolarizedStyle, LightGreenStyle, Style

client = MongoClient()
db = client.cnu
locations = db.locations
updates = db.updates
graphs = db.graphs
cursor = updates.find()
time = strftime("%H:%M")
displayTime = strftime("%I:%M%P")
timeKey = int(strftime("%H%M"))
info = []

def get_recursive_locations():
    return recursive_locations([], locations.find())

def recursive_locations(build, locs):
    for loc in locs:
        loc = loads(dumps(loc))
        build.append(loc)
        if len(loc.get('subLocations')) > 0:
            recursive_locations(build, loc.get('subLocations'))
    return build

for record in cursor:
    location = record.get('location')
    found = False
    for i in info:
        if i.get('location') == location:
            found = True
            people = i.get('people')
            i.update({'people':people+1})
    if not found:
        info.append({'location':location,'people':1})
for location in get_recursive_locations():
    loc = location.get('name')
    people = 0
    for i in info:
        if i.get('location') == loc:
            people = i.get('people')
    insert = {'id':time + "_" + loc, 'key':timeKey, 'time':time, 
'displayTime':displayTime, 'location':loc, 'people':people}
    key = {'id':time + "_" + loc}
    graphs.update(key, insert, upsert=True)

    # Generate graph
    
    graph = graphs.find({'location': loc}).sort("key", pymongo.ASCENDING)
    obj = loads(dumps(graph))

    style = Style(
        background='#DFDFD7',
        plot_background='#DFDFD7'',
        foreground='#333333',
        foreground_light='#666',
        foreground_dark='#222222',
        opacity='.5',
        opacity_hover='.9',
        transition='250ms ease-in',
        colors=(
            '#7dcf30', '#247fab', lighten('#7dcf30', 10), '#ccc',
            darken('#7dcf30', 15), '#ddd', lighten('#247fab', 10),
            darken('#247fab', 15)))


    config = Config()
    config.show_legend = False
    config.fill = True
    config.style = style
    config.x_label_rotation = 80
    config.show_only_major_dots = True
    config.x_labels_major_every = 2
    config.show_minor_x_labels = False
    config.show_minor_y_labels = False
    config.major_label_font_size = 12
    config.print_values = False
    #config.print_zeroes = True
    #config.y_scale = 1
    #config.order_min = 1
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
    chart.render_to_file('/var/www/api.gravitydevelopment.net/cnu/static/graphs/' + loc + '.svg')
