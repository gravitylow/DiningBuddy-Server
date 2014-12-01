#!/usr/bin/python
import sys
import os
import logging

dir = "/var/www/api.gravitydevelopment.net/cnu"

logging.basicConfig(filename=dir+'/logs/app.log',format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',datefmt='%H:%M:%S',level=logging.DEBUG)

sys.path.insert(0, dir)

ADMINS = ['adam.fendley@gmail.com']

from cnu import app as application
application.secret_key = '41Sy%6kvbf4AW4oOMo#NaYnZFKxE3Z'
application.static_url_path = ''

if application.debug:
    print('debug!')
    from logging.handlers import SMTPHandler
    from logging.handlers import RotatingFileHandler

    mail_handler = SMTPHandler('127.0.0.1',
                               'server-error@api.gravitydevelopment.net',
                               ADMINS, 'CNU Failed')
    mail_handler.setLevel(logging.ERROR)

    file_handler = RotatingFileHandler(dir + '/logs/app.log', maxBytes=5000, backupCount=5)
    file_handler.setLevel(logging.WARNING)
    applocation.logger.addHandler(file_handler)
    application.logger.addHandler(mail_handler)

    application.logger.warning("This is test log line")
