import sys
import pushbullet

from datetime import datetime
import reading

# initialize system reading for reading environment
sysreader = reading.Reading()
# get reading from environment
reading = sysreader.getReading()

devices = []
# Check if another notification exist today
try:
    history = bluetoothdb.BluetoothDB()
    devices = bluetoothdb.getDevices()
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
