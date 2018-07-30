from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from sense_hat import SenseHat
import json

sense = SenseHat()
sense.clear()

temp = sense.get_temperature()
humidity = sense.get_humidity()
data = {
    "humidity": humidity,
    "temperature": temp,
}
dataStr = json.dumps(data)
print(data)
myMQTTClient = AWSIoTMQTTClient("raspberry-RMIT")
myMQTTClient.configureEndpoint("a2jwan9azy4oaj.iot.ap-southeast-2.amazonaws.com", 8883)
myMQTTClient.configureCredentials("./root-ca.pem", "./f3ed0017cd-private.pem.key", "./f3ed0017cd-certificate.pem.crt")
myMQTTClient.connect()
myMQTTClient.publish("rmit", dataStr, 0)
myMQTTClient.disconnect()