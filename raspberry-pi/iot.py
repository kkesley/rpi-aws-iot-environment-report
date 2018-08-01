import iotcore
import reading
import json

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
except:
    print("Cannot publish to iot core")
