# website-check

A simple stand-alone Web service for monitoring websites

The code is runnable as a stand-alone Web server.

### Dependencies
* Python 2.7
* web.py python module
* python requests

### Installation
1. Get the code
2. Install web.py `pip install web.py`
2. Install requests `pip install requests`

### Configuration
Set the following variables in website-check.py

1. poll_interval (how often each site should be checked)
2. max_fails (maximum number of times a site can fail the check before email notification
3. gmail_user = '' (your gmail email address)
4. gmail_pwd = '' (your gmail password)
5. recipients = \['someone@example.com', 'someone@example.com'\] (who email should be sent to)

You can also use a smtp server other than gmail. Just set the values appropriately and see [Python's smtplib documentation](http://docs.python.org/2/library/smtplib.html) for more details.

### Run
There are two options: either specify URLs and assertion strings at runtime (use "" for no assertion), or specify a text file that contains comma separated URLs and assertion strings.

1. `python website-check.py port "site1" "assert1" ["site2" "assert2" ... ]`
2. `python website-check.py port servers.txt

Sample servers.txt

<pre>
http://www.google.com,I'm feeling lucky
http://www.yahoo.com,Yahoo
http://www.bing.com,
</pre>

Navigate to http://localhost:port to view...
