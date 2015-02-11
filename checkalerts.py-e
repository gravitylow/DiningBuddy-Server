#!flask/bin/python
from pymongo import MongoClient
from cnu import app
import imaplib
import email

logger = app.logger

client = MongoClient()
db = client.cnu
alerts = db.alerts

def process_mailbox(M):
    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print "No messages found!"
        return

    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print "ERROR getting message", num
            return
        msg = email.message_from_string(data[0][1])
        title = 'CNU ALERT: %s' % (msg['Subject'])
        value = {"title": title, "target_os": "all", "target_version": "all", "target_time_min": 0, "target_time_max": 0}
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True) #to control automatic email-style MIME decoding (e.g., Base64, uuencode, quoted-printable)
                    body = body.decode()
                    value['message'] = body

        key = {"title": title}
        alerts.update(key, value, upsert=True)

M = imaplib.IMAP4_SSL('imap.gmail.com')
try:
    M.login('cnudiningbuddy@gmail.com', '**REMOVED**')
except imaplib.IMAP4.error:
    print "LOGIN FAILED!!! "
    sys.exit(0)

rv, mailboxes = M.list()
if rv == 'OK':
    rv, data = M.select("CNUALERT")
if rv == 'OK':
    process_mailbox(M) # ... do something with emails, see below ...
    M.close()
M.logout()
