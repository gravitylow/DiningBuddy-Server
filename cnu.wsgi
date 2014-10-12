#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/api.gravitydevelopment.net/cnu")

from cnu import app as application
application.secret_key = '41Sy%6kvbf4AW4oOMo#NaYnZFKxE3Z'
application.static_url_path = ''
