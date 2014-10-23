#!flask/bin/python
import urllib
import urllib2
import simplejson
import pprint
import os
import dateutil.parser
from datetime import datetime, timedelta, date
import pytz
import json
from apiclient.discovery import build

regattas_id = 'dining@cnu.edu'
commons_id = 'cnu.edu_tjpup58u1v03ijvc91uof8qmq0@group.calendar.google.com'
key = '**REMOVED**'

today = datetime.now(pytz.timezone('US/Eastern'))
today = today.replace(hour=0, minute=0, second=0)

regattas = {}
commons = {}

service = build('calendar', 'v3', developerKey=key)
request = service.events().list(calendarId=regattas_id, timeMin=today.isoformat(), timeMax=(today + timedelta(days=1)).isoformat(), singleEvents=True, userIp='2602:ffea:a::580b:b2c3')
while request != None:
    response = request.execute()
    for event in response.get('items', []):
      summary = event.get('summary')
      description = event.get('description')
      start = dateutil.parser.parse(event.get('start').get('dateTime')).strftime('%I:%M%p').lstrip("0")
      end = dateutil.parser.parse(event.get('end').get('dateTime')).strftime('%I:%M%p').lstrip("0")
      time = int(dateutil.parser.parse(event.get('start').get('dateTime')).strftime('%H'))

      dictionary = {}
      dictionary['summary'] = summary
      dictionary['description'] = description
      dictionary['start'] = start
      dictionary['end'] = end
      regattas[time] = dictionary
    request = service.events().list_next(request, response)

request = service.events().list(calendarId=commons_id, timeMin=today.isoformat(), timeMax=(today + timedelta(days=1)).isoformat(), singleEvents=True)
while request != None:
    response = request.execute()
    for event in response.get('items', []):
      summary = event.get('summary')
      description = event.get('description')
      start = dateutil.parser.parse(event.get('start').get('dateTime')).strftime('%I:%M%p').lstrip("0")
      end = dateutil.parser.parse(event.get('end').get('dateTime')).strftime('%I:%M%p').lstrip("0")
      time = int(dateutil.parser.parse(event.get('start').get('dateTime')).strftime('%H'))

      dictionary = {}
      dictionary['summary'] = summary
      dictionary['description'] = description
      dictionary['start'] = start
      dictionary['end'] = end
      commons[time] = dictionary
    request = service.events().list_next(request, response)

regattas_new = []
commons_new = []

for value in sorted(regattas):
    regattas_new.append(regattas.get(value))

for value in sorted(commons):
    commons_new.append(commons.get(value))

file = open('static/menus/Regattas.txt', 'w')
file.write(json.dumps(regattas_new))
file.close()
file = open('static/menus/Commons.txt', 'w')
file.write(json.dumps(commons_new))
file.close()
