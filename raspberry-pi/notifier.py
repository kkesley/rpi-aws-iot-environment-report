import sys
import pushbullet

from datetime import datetime
import reading

# initialize system reading for reading environment
sysreader = reading.Reading()
# get reading from environment
reading = sysreader.getReading()

# exit the program if the temperature is more than 20
if(reading["temperature"] > 20):
    sys.exit(0)


# Check if another notification exist today
try:
    history = notificationdb.NotificationDB()
    if(history.checkTodayNotifications() != True):
        sys.exit(0)
except (exceptions.InfluxDBClientError, exceptions.InfluxDBServerError) as err:
    # Exception from influx, print it but proceed to notify the user anyway
    print(err)

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

# Write the history for all devices
try:
    history.writeHistory(devices, reading["temperature"], reading["deviceid"])
except (exceptions.InfluxDBClientError, exceptions.InfluxDBServerError) as err:
    print(err)
