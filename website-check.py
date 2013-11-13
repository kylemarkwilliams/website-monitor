"""
@author Kyle Williams <kwilliams@psu.edu>
@date Nov 12, 2013

A simple Web service to monitor a set of websites

Run: python website-check.py port site1 [site2 ... ]
"""

import web
import requests
import sys
import thread
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from datetime import datetime
from repeattimer import RepeatTimer

urls = (
'/', 'Index',
)

poll_interval = 300 #How often the sites should be polled
max_fails = 10
servers = []
app = web.application(urls, globals(), servers)

gmail_user = ''
gmail_pwd = ''

def mail(to, subject, text):
   msg = MIMEMultipart()
   msg['From'] = gmail_user
   msg['To'] = to
   msg['Subject'] = subject
   msg.attach(MIMEText(text))  
   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(gmail_user, gmail_pwd)
   mailServer.sendmail(gmail_user, to, msg.as_string())   
   mailServer.close()

def check_servers():
    """ A static method to check the status of all servers """
    for server in servers: 
      thread.start_new_thread(server.check_status, ())
      
class Server:
  def __init__(self, url):
    self.url = url
    self.fails = 0
    self.status_code = 0
    self.status = ''
    self.last_checked=datetime.min
    self.notified_fail=False
    
  def check_status(self):
    """ Checks the status of the server """
    self.last_checked = datetime.now()
    try:
      r = requests.get(self.url, timeout=5)
      self.status_code = r.status_code
      if self.status_code == 200:
	self.status = 'OK'
	self.fails = 0
	self.notified_fail=False
      else:
	self.fails += 1
	self.status = 'ERROR'
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
      self.status_code = 503
      self.status = str(e)
      self.fails += 1
    
    if self.fails >= max_fails and self.notified_fail is False:
      print self.notified_fail
      self.notified_fail = True
      mail('kwilliams@psu.edu', 'Server down', str("Server at " + self.url + " is down. Last checked at " + str(self.last_checked)))
      print self.notified_fail
      
    print str(self.last_checked) + ": " + self.url + " - " + self.status
    
    return self.status_code, self.last_checked
    
class Index:

  def GET(self):    
    """ The display page """
    web.header('Content-Type','text/html; charset=utf-8') 
    html = """<html><body><h3>Status of Web Servers</h3>"""
    for server in servers:
      html += '<b>Server:</b> ' + server.url + '<br />'
      html += '<b>Status:</b> ' + str(server.status_code) + ' ' + server.status + '<br />'
      html += '<b>Last Checked:</b> ' + str(server.last_checked) + '<br /><br />'
    html += """<form method="POST" action="">
                <input type="submit" value="Check Status"/>
                </form>
                </body></html>"""
    return html
    
  def POST(self):
    """ Manual check """
    check_servers()
    raise web.seeother('/')
    
if __name__ == "__main__":
  
  for arg in sys.argv[2:]:
    servers.append(Server(arg))
  check_servers()
  timerName = RepeatTimer(poll_interval, check_servers) # Repeatedly check servers
  timerName.start()
  app.run()
  
