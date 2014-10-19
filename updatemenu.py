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

regattas = []
commons = []

service = build('calendar', 'v3', developerKey=key)
request = service.events().list(calendarId=regattas_id, timeMin=today.isoformat(), timeMax=(today + timedelta(days=1)).isoformat(), singleEvents=True, userIp='2602:ffea:a::580b:b2c3')
while request != None:
    response = request.execute()
    for event in response.get('items', []):
      summary = event.get('summary')
      description = event.get('description')
      start = dateutil.parser.parse(event.get('start').get('dateTime')).strftime('%I:%M%p').lstrip("0")
      end = dateutil.parser.parse(event.get('end').get('dateTime')).strftime('%I:%M%p').lstrip("0")

      dictionary = {}
      dictionary['summary'] = summary
      dictionary['description'] = description
      dictionary['start'] = start
      dictionary['end'] = end
      regattas.append(dictionary)
    request = service.events().list_next(request, response)
file = open('static/menus/regattas.txt', 'w')
file.write(json.dumps(regattas))
file.close()

request = service.events().list(calendarId=commons_id, timeMin=today.isoformat(), timeMax=(today + timedelta(days=1)).isoformat(), singleEvents=True)
while request != None:
    response = request.execute()
    for event in response.get('items', []):
      summary = event.get('summary')
      description = event.get('description')
      start = dateutil.parser.parse(event.get('start').get('dateTime')).strftime('%I:%M%p').lstrip("0")
      end = dateutil.parser.parse(event.get('end').get('dateTime')).strftime('%I:%M%p').lstrip("0")

      dictionary = {}
      dictionary['summary'] = summary
      dictionary['description'] = description
      dictionary['start'] = start
      dictionary['end'] = end
      commons.append(dictionary)
    request = service.events().list_next(request, response)
file = open('static/menus/commons.txt', 'w')
file.write(json.dumps(commons))
file.close()
