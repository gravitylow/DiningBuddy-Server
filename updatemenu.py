#!/usr/bin/env python
import urllib
import urllib2
import simplejson
import pprint
import os
from apiclient.discovery import build

regattas_id = 'dining@cnu.edu'
commons_id = 'cnu.edu_tjpup58u1v03ijvc91uof8qmq0@group.calendar.google.com'
key = '**REMOVED**'

service = build('calendar', 'v3', developerKey=key)
request = service.events().list(calendarId=regattas_id)
while request != None:
    response = request.execute()
    for event in response.get('items', []):
      print repr(event.get('summary', 'NO SUMMARY')) + '\n'
    request = service.events().list_next(request, response)
