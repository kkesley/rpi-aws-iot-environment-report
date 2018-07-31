import iotcore
import reading
import json

sysreader = reading.Reading()
data = sysreader.getReading()
dataStr = json.dumps(data)
print(dataStr)
iotConnector = iotcore.IOTCore()
iotConnector.publish("rmit", dataStr)
iotConnector.disconnect()