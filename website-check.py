"""
@author Kyle Williams <kwilliams@psu.edu>
@date Nov 12, 2013

A simple Web service to monitor a set of websites

Run: python website-check.py port site1 [site2 ... ]
"""

import web
import requests
import sys
from datetime import datetime
from repeattimer import RepeatTimer

urls = (
'/', 'Index',
)

poll_interval = 300 #How often the sites should be polled

servers = []
app = web.application(urls, globals(), servers)

class ServerCheck(object):
  @staticmethod
  def check_servers():
    """ A static method to check the status of all servers """
    for server in servers: 
      server.check_status()

class Server:
  def __init__(self, url):
    self.url = url
    self.fails = 0
    self.status_code = 0
    self.status = ''
    self.last_checked=datetime.min
    
  def check_status(self):
    """ Checks the status of the server """
    self.last_checked = datetime.now()
    try:
      r = requests.get(self.url)
      self.status_code = r.status_code
      if self.status_code == 200:
	self.status = 'OK'
    except requests.exceptions.ConnectionError as e:
      self.status_code = 404
      self.status = str(e)
      
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
    ServerCheck.check_servers()
    return self.GET()
    
if __name__ == "__main__":
  
  for arg in sys.argv[2:]:
    servers.append(Server(arg))
  ServerCheck.check_servers()
  timerName = RepeatTimer(poll_interval, ServerCheck.check_servers) # Repeatedly check servers
  timerName.start()
  app.run()
