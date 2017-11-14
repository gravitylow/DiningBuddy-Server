#!flask/bin/python
import simplejson
import pprint
import os
import dateutil.parser
import pytz
import json
import config as app_config
from apiclient.discovery import build
from datetime import datetime, timedelta, date

today = datetime.now(pytz.timezone('America/New_York'))
today = today.replace(hour=0, minute=0, second=0, microsecond=0)
tomorrow = today + timedelta(days=1)
today = today.isoformat()
tomorrow = tomorrow.isoformat()

regattas = {}
commons = {}

service = build('calendar', 'v3', developerKey=app_config.GOOGLE_CALENDAR_KEY)
request = service.events().list(calendarId=app_config.GOOGLE_CALENDAR_REGATTAS_ID, timeMin=today, timeMax=tomorrow, singleEvents=True)
while request != None:
    response = request.execute()
    for event in response.get('items', []):
        summary = event.get('summary')
        description = event.get('description')
        start = dateutil.parser.parse(event.get('start').get('dateTime')).strftime('%I:%M%p').lstrip("0")
        end = dateutil.parser.parse(event.get('end').get('dateTime')).strftime('%I:%M%p').lstrip("0")
        time = int(dateutil.parser.parse(event.get('start').get('dateTime')).strftime('%s'))

        dictionary = {}
        dictionary['summary'] = summary
        dictionary['description'] = description
        dictionary['start'] = start
        dictionary['end'] = end
        regattas[time] = dictionary
    request = service.events().list_next(request, response)

request = service.events().list(calendarId=app_config.GOOGLE_CALENDAR_COMMONS_ID, timeMin=today, timeMax=tomorrow, singleEvents=True)
while request != None:
    response = request.execute()
    for event in response.get('items', []):
        summary = event.get('summary')
        description = event.get('description')
        start = dateutil.parser.parse(event.get('start').get('dateTime')).strftime('%I:%M%p').lstrip("0")
        end = dateutil.parser.parse(event.get('end').get('dateTime')).strftime('%I:%M%p').lstrip("0")
        time = int(dateutil.parser.parse(event.get('start').get('dateTime')).strftime('%s'))

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

file = open(app_config.APP_DIRECTORY + 'static/menus/Regattas.txt', 'w')
file.write(json.dumps(regattas_new))
file.close()
file = open(app_config.APP_DIRECTORY + 'static/menus/Commons.txt', 'w')
file.write(json.dumps(commons_new))
file.close()
