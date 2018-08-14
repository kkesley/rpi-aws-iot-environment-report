import sys
import pushbullet
from influxdb import exceptions
from datetime import datetime
import reading
import notificationdb

def main():
    # initialize system reading for reading environment
    sysreader = reading.Reading()
    # get reading from environment
    reader = sysreader.getReading()

    # exit the program if the temperature is more than 20
    if(reader["temperature"] > 20):
        print(reader["temperature"])
        sys.exit(0)


    # Check if another notification exist today
    try:
        history = notificationdb.NotificationDB()
        if(history.checkTodayNotifications() != True):
            sys.exit(0)
    except FileNotFoundError:
        # config file not found
        print("config file not found. aborting")
        sys.exit(0)
    except KeyError:
        # config file is misconfigured / corrupted
        print("miconfigured key in config file")
        sys.exit(0)
    except (exceptions.InfluxDBClientError, exceptions.InfluxDBServerError) as err:
        # Exception from influx, print it but proceed to notify the user anyway
        print(err)

    # send push bullet notification. It's too cold!
    devices = []
    try:
        pusher = pushbullet.PushBullet()
        pusher.pushNotification(reader["temperature"], "cold")
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
        history.writeHistory(devices, reader["temperature"], reader["deviceid"])
    except (exceptions.InfluxDBClientError, exceptions.InfluxDBServerError) as err:
        print(err)

main()