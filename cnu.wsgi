#!/usr/bin/python
import sys
import logging

dir = "/var/www/api.gravitydevelopment.net/cnu"

logging.basicConfig(filename=dir+'/logs/app.log',format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',datefmt='%H:%M:%S',level=logging.DEBUG)

sys.path.insert(0, dir)

ADMINS = ['adam.fendley@gmail.com']

from cnu import app as application
application.secret_key = '41Sy%6kvbf4AW4oOMo#NaYnZFKxE3Z'
application.static_url_path = ''

if not application.debug:
    print('debug!')
    from logging.handlers import SMTPHandler

    mail_handler = SMTPHandler('127.0.0.1',
                               'server-error@api.gravitydevelopment.net',
                               ADMINS, 'CNU Failed')
    mail_handler.setLevel(logging.ERROR)

    application.logger.addHandler(mail_handler)

    application.logger.error("This is test error")
