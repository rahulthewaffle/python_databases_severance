import urllib.request, urllib.parse, urllib.error
import http
import sqlite3
import json
import time
import ssl
import sys

api_key = False
# If you have a Google Places API key, enter it here
# api_key = 'AIzaSy___IDByT70'

if api_key is False:
    api_key = 42
    serviceurl = "http://py4e-data.dr-chuck.net/json?"
else :
    serviceurl = "https://maps.googleapis.com/maps/api/geocode/json?"

# Additional detail for urllib
# http.client.HTTPConnection.debuglevel = 1

conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)''')
#note that there is no autoincrementing integer PK on this table! Since there is no PK at the 0 index of a returned row, address and geodata are accessed at the 0 and 1 index.

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

fh = open("where.data")

count = 1
countLimit = 5 #batch size
pauseCount = 10 #number of requests before briefly pausing requests

for line in fh:
    print('')

    if count > countLimit :
        print('Retrieved', countLimit, 'locations, restart to retrieve more')
        break

    address = line.strip() #extract address from line
    cur.execute("SELECT geodata FROM Locations WHERE address= ?", #query for address
        (memoryview(address.encode()), ))

    try: #see if address exists
        data = cur.fetchone()[0]
        print("Found in database ",address)
        continue #skip address if found in database
    except:
        pass

    parms = dict()
    parms["address"] = address
    if api_key is not False: parms['key'] = api_key
    url = serviceurl + urllib.parse.urlencode(parms) #construct url with encoded params

    print('Retrieving', url)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters', data[:20].replace('\n', ' ')) #debugging statement - "We got something or we made a bad request"
    print('Request count at', count)
    count = count + 1 #increment to batch limit

    try:
        js = json.loads(data)
    except:
        print(data)  # We print in case unicode causes an error
        continue

    if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS') :
        print('==== Failure To Retrieve ====')
        print(data)
        break

    cur.execute('''INSERT INTO Locations (address, geodata)
            VALUES ( ?, ? )''', (memoryview(address.encode()), memoryview(data.encode()) ) )
    conn.commit()
    if count % pauseCount == 0 :
        print('Pausing for a bit...')
        time.sleep(5)

print("Run geodump.py to read the data from the database so you can vizualize it on a map.")
