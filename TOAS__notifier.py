# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 13:32:26 2017

@author: secoder
"""

import urllib2
import HTMLParser
import hashlib
import io
import os.path

class TableParser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.in_td = False
        self.result = []
     
    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.in_td = True
     
    def handle_data(self, data):
        if self.in_td:
           #print data
           self.result.append(data)

     
    def handle_endtag(self, tag):
        if tag == 'table':
            self.in_td = False

'''
use gmail smtp to send the notification email

user:
    your gmail user name
pwd:
    your gmail password
recipient:
    the receiver email address
subject:
    the notification email subject
body:
    the notification email body
'''
def send_email(user, pwd, recipient, subject, body):
    import smtplib

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        # SMTP_SSL Example
        server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server_ssl.ehlo() # optional, called by login()
        server_ssl.login(gmail_user, gmail_pwd)  
        # ssl server doesn't support or need tls, so don't call server_ssl.starttls() 
        server_ssl.sendmail(FROM, TO, message)
        #server_ssl.quit()
        server_ssl.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"        

"""
check if there is digtial in the string
"""
def digstring(s):
    for i in s:
        if i.isdigit():
            return True
    return False
    
"""
 htmlcontent is the parser.result
"""
def send_notification(htmlcontent):
    
    # clean the parser result by removing alll the '\n'
    info =[e for e in htmlcontent if e != '\n']
    msg = []

    i = 0
    while i != len(info):
        t = info[i:i+5]
        i = i + 5
        if digstring(t[-1]):
            t.append(info[i])
            i = i + 1 
            t = '  '.join(t) + '\n'
            msg.append(t)

    msg=' '.join(msg)

    send_email('pwd','uername','xxxx@zzzz.com','NEW Available Rooms',msg)


"""
Start
"""

if __name__ == '__main__':
    # get the webpage content        
    response = urllib2.urlopen('http://toas.fi/en/quickly-available-apartments/')
    html = response.read()
    
    # parser the table tag in the content
    p = TableParser()
    p.feed(html)
    
    # generate hash for the info
    hash_object = hashlib.sha256(str(p.result))
    hex_dig = hash_object.hexdigest()
    
    path = './lashHash'
    
    if os.path.exists(path):
        with io.open(path, 'r+', encoding="utf-8") as f:
            read_data = f.read()
            print 'new  hash: ' + hex_dig
            print 'last hash: ' + read_data
    
            if hex_dig == read_data:
                # information didn't change, do nothing and return
                f.close()
            else:
                # information changed, send notification email 
                send_notification(p.result)
                # update the hash
                f.seek(0)
                f.write(hex_dig.decode('utf-8'))
                f.close()
    else:
        with io.open(path, 'w', encoding="utf-8") as f:
            f.write(hex_dig.decode('utf-8'))
            f.close()
            # the first run, send the first notification
            send_notification(p.result)
        







