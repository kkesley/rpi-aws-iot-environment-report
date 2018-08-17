import sys
import pushbullet
from influxdb import exceptions
from datetime import datetime
import reading
import bluetoothdb
import bluetooth
import time

# Search for device based on device's name
def search(reader, devices, pusher, history):
    while True:
        nearby_devices = bluetooth.discover_devices() # get all nearby devices
        eligibleMacs = list(map(lambda d: d["MAC"], devices)) # convert devices to list of macs
        registered_devices = list(set(nearby_devices) & set(eligibleMacs)) # get the intersection of eligible devices and available devices
        if len(registered_devices) > 0:
            try:
                # if pushbullet and db exist, continue
                if pusher is not None and history is not None:
                    pushed_devices = []
                    for device in registered_devices:
                        try:
                            devObj = list(filter(lambda d: d["MAC"] == device, devices))[0] # get the device with a given MAC address
                            iden = devObj["pushbullet_iden"] # get the device_iden of pushbullet
                            name = devObj["name"] # get the person name
                            pusher.pushNotification(reader["temperature"], "bt", name=name, device=iden) # send the notification to the person
                            pushed_devices.append(device) # successfully pushed
                        except IndexError as err:
                            print(err)
                            continue
                        except KeyError:
                            print("please check your configuration file")
                            continue
                        except:
                            print("Fail to call pushbullet API")
                            continue
                    history.writeHistory(pushed_devices, reader["temperature"], reader["deviceid"]) # write history for all successfull pushes
            except (exceptions.InfluxDBClientError, exceptions.InfluxDBServerError) as err:
                print(err)
            break
        time.sleep(3) #Sleep three seconds 

def main():
    # initialize system reading for reading environment
    sysreader = reading.Reading()
    # get reading from environment
    reader = sysreader.getReading()

    history = None
    devices = []
    sentDevices = []
    eligibleMacs = []
    # Check if another notification exist today
    try:
        history = bluetoothdb.BluetoothDB()
        devices = history.readDevices()
        macs = list(map(lambda d: d["MAC"], devices)) # list all macs listed in the config
        sentDevices = history.getHistory() # list all not eligible devices (already sent)
        eligibleMacs = list(set(macs) - set(sentDevices)) # remove all devices which already been sent
        devices = list(filter(lambda d: d["MAC"] in eligibleMacs, devices)) # get all eligible devices
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
    pusher = None
    try:
        pusher = pushbullet.PushBullet() #instantiate pushbullet
    except KeyError:
        print("please check your configuration file")
    except FileNotFoundError:
        print("config file not found")

        
    if(history is not None and len(devices) > 0):
        # search bluetooth devices
        search(reader, devices, pusher, history)


main()