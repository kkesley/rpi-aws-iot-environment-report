import iotcore
import reading
import json
import time

def main():
    # initialize system reading for reading environment
    sysreader = reading.Reading()

    # get reading from environment
    data = sysreader.getReading()
    dataStr = json.dumps(data)
    print(dataStr)

    try:
        # initialize iot connection
        iotConnector = iotcore.IOTCore()
        # publish data to iot
        iotConnector.publish("rmit", dataStr)
        # disconnect from iot
        iotConnector.disconnect()
    except KeyError:
        print("Invalid config file")
    except FileNotFoundError:
        print("config file not found")
    except:
        print("Cannot publish to iot core")

while True:
    main()
    time.sleep(20)
