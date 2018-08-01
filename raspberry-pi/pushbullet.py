from urllib import request, parse, error
import json
class PushBullet:
    def __init__(self):
        self.access_token = "" # pushbullet access token
        self.push_message = {} # push message dict
        self.push_url = "" # url for pushing notification
        self.device_url = "" # url for getting devices list
        self.config = {} # config placeholder
        # read the config file
        try:
            config_file = open('./config/pushbullet.json')
            # parse the content into dictionary
            self.config = json.loads(config_file.read())
        except FileNotFoundError:
            print("file not found")
            raise
        try:
            # initialize object variable from config
            self.access_token = self.config["access-token"]
            self.push_message = self.config["message"]
            self.push_url = self.config["push-url"]
            self.device_url = self.config["device-url"]
        except KeyError:
            print("key error")
            raise

    def pushNotification(self, temperature, device = None):
        # construct data for pushbullet api
        try:
            if(device != None):
                # target specific device
                self.push_message["device_iden"] = device
            #format body to display current temperature
            self.push_message["body"] = self.push_message["body"].format(temperature)
        except KeyError:
            print("key error")
            raise

        data = json.dumps(self.push_message).encode()
        #construct request object for pushbullet api
        req =  request.Request(self.push_url, data=data) # this will make the method "POST"
        req.add_header('Content-Type', 'application/json')
        req.add_header('Access-Token', self.access_token)
        try:
            # send request to pushbullet api
            resp = request.urlopen(req)
        except error.URLError:
            print("invalid url")
            raise
        except error.HTTPError as err:
            # pushbullet api return error
            print(err)
            raise

    def getDevices(self):
        req = request.Request(self.device_url)
        req.add_header('Access-Token', self.access_token)
        resp = None
        try:    
            resp = request.urlopen(req)
        except error.URLError:
            print("invalid url")
            raise
        except error.HTTPError as err:
            print(err)
            raise

        devices = []
        try:
            body = json.loads(resp.read().decode())
            for device in body["devices"]:
                devices.append(device["iden"])
        except TypeError as err:
            print(err)
            raise
        except KeyError as err:
            print(err)
            raise
        return devices
