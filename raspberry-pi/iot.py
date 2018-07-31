from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from sense_hat import SenseHat
import deviceid
import json
import time

sense = SenseHat()
sense.clear()

temperature = sense.get_temperature()
humidity = sense.get_humidity()
pressure = sense.get_pressure()
data = {
    "deviceid": deviceid.getserial(),
    "humidity": humidity,
    "pressure": pressure,
    "temperature": temperature,
    "timestamp": int(round(time.time() * 1000)),
}
dataStr = json.dumps(data)
myMQTTClient = AWSIoTMQTTClient("raspberry-RMIT")
myMQTTClient.configureEndpoint("a2jwan9azy4oaj.iot.ap-southeast-2.amazonaws.com", 8883)
myMQTTClient.configureCredentials("./root-ca.pem", "./f3ed0017cd-private.pem.key", "./f3ed0017cd-certificate.pem.crt")
myMQTTClient.connect()
myMQTTClient.publish("rmit", dataStr, 0)
myMQTTClient.disconnect()