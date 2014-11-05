#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/api.gravitydevelopment.net/cnu")

ADMINS = ['adam.fendley@gmail.com']

from cnu import app as application
application.secret_key = '41Sy%6kvbf4AW4oOMo#NaYnZFKxE3Z'
application.static_url_path = ''

if not application.debug:
    import logging
    from logging.handlers import SMTPHandler
    mail_handler = SMTPHandler('127.0.0.1',
                               'server-error@api.gravitydevelopment.net',
                               ADMINS, 'CNU Failed')
    mail_handler.setLevel(logging.ERROR)
    application.logger.addHandler(mail_handler)
