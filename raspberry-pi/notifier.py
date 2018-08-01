from urllib import request, parse, error
import json
import sys

# get reading from environment
reading = sysreader.getReading()

# exit the program if the temperature is more than 20
if(reading["temperature"] > 20):
    sys.exit(0)

# construct data for pushbullet api
data = json.dumps({
    "body": "It's cold out there! {0} degree requires you to wear a scarf!".format(20),
    "title": "Winter is coming!",
    "type": "note",
    "device_iden": "ujwIuCpOtZQsjAiVsKnSTs"
}).encode()

#construct request object for pushbullet api
req =  request.Request("https://api.pushbullet.com/v2/pushes", data=data) # this will make the method "POST"
req.add_header('Content-Type', 'application/json')
req.add_header('Access-Token', 'o.bZVwCzdieYn1BLxTUwN12Q08oSMpyEB9')
try:
    # send request to pushbullet api
    resp = request.urlopen(req)
except error.HTTPError as err:
    # pushbullet api return error
    print(err)
