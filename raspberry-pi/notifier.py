import sys
import pushbullet
from influxdb import InfluxDBClient
from datetime import datetime
import reading

# initialize system reading for reading environment
sysreader = reading.Reading()
# get reading from environment
reading = sysreader.getReading()

# exit the program if the temperature is more than 20
if(reading["temperature"] > 20):
    sys.exit(0)

client = InfluxDBClient('localhost', 8086, 'kendrick', 'iotrmit', 'environment')
result = client.query('select count(device) from notification_history where time >  now() - 1d group by time(1d) order by time desc limit 1')
for item in result.get_points("notification_history"):
    if(item["count"] > 0):
        sys.exit(0)

# send push bullet notification. It's too cold!
devices = []
try:
    pusher = pushbullet.PushBullet()
    pusher.pushNotification(reading["temperature"])
    devices = pusher.getDevices()
except KeyError:
    print("please check your configuration file")
except TypeError:
    print("cannot decode body")
except FileNotFoundError:
    print("config file not found")
except:
    print("Fail to call pushbullet API")

if(len(devices) <= 0):
    sys.exit(0)

data = []
for device in devices:
    data.append({
        "measurement": "notification_history",
        "tags": {
            "host": "server01",
            "region": "ap-southeast-2"
        },
        "time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        "fields": {
            "device": device
        }
    })
client.write_points(data)