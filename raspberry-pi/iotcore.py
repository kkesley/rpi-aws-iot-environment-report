from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
class IOTCore:
    def __init__(self):
        config_file = open('aws-iot.json')
        config = json.loads(config_file.read())
        print(config)
        
        # connect to iot
        try:
            self.client = AWSIoTMQTTClient(config["client"])
            self.client.configureEndpoint(config["host"], config["port"])
            self.client.configureCredentials(config["root-ca"], config["private-key"], config["certificate"])
            self.client.connect()
        except KeyError:
            print("Key not found")
            raise
        except (AWSIoTPythonSDK.exception.operationTimeoutException, AWSIoTPythonSDK.exception.operationError) as err:
            print(err)
            raise
        except:
            print("unknown error")
    
    def publish(self, key, data):
        # publish data to iot
        try:
            self.client.publish(key, data, 0)
        except (AWSIoTPythonSDK.exception.operationTimeoutException, AWSIoTPythonSDK.exception.operationError) as err:
            print(err)
            raise
        except:
            print("unknown error")
    
    def disconnect(self):
        # disconnect from iot
        self.client.disconnect()