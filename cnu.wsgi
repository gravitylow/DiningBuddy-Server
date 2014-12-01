#!/usr/bin/python
import sys
import os

dir = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(0, dir)

ADMINS = ['adam.fendley@gmail.com']

from cnu import app as application
application.secret_key = '41Sy%6kvbf4AW4oOMo#NaYnZFKxE3Z'
application.static_url_path = ''

if application.debug:
    import logging
    from logging.handlers import SMTPHandler
    from logging.handlers import RotatingFileHandler

    mail_handler = SMTPHandler('127.0.0.1',
                               'server-error@api.gravitydevelopment.net',
                               ADMINS, 'CNU Failed')
    mail_handler.setLevel(logging.ERROR)

    file_handler = RotatingFileHandler(dir + 'logs/app.log')
    file_handler.setLevel(logging.WARNING)
    applocation.logger.addHandler(file_handler)
    application.logger.addHandler(mail_handler)
