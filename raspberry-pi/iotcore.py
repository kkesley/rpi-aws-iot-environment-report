from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
class IOTCore:
    def __init__(self):
        # connect to iot
        self.client = AWSIoTMQTTClient("raspberry-RMIT")
        self.client.configureEndpoint("a2jwan9azy4oaj.iot.ap-southeast-2.amazonaws.com", 8883)
        self.client.configureCredentials("./root-ca.pem", "./f3ed0017cd-private.pem.key", "./f3ed0017cd-certificate.pem.crt")
        self.client.connect()
    
    def publish(self, key, data):
        # publish data to iot
        self.client.publish(key, data, 0)
    
    def disconnect(self):
        # disconnect from iot
        self.client.disconnect()