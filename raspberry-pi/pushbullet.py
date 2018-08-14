from urllib import request, parse, error
import json
import copy
class PushBullet:
    def __init__(self):
        self.access_token = "" # pushbullet access token
        self.message_set = {} # push message dict
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
            self.message_set = self.config["message_set"]
            self.push_url = self.config["push-url"]
            self.device_url = self.config["device-url"]
        except KeyError:
            print("key error")
            raise

    def pushNotification(self, temperature, message_set, name = '', device = None):
        # construct data for pushbullet api
        message = copy.copy(self.message_set[message_set])
        try:
            if(device != None):
                # target specific device
                message["device_iden"] = device
            #format body to display current temperature
            message["body"] = self.message_set[message_set]["body"].format(temperature, name)
                
            
        except KeyError:
            print("key error")
            raise

        data = json.dumps(message).encode()
        #construct request object for pushbullet api
        req =  request.Request(self.push_url, data=data) # this will make the method "POST"
        req.add_header('Content-Type', 'application/json')
        req.add_header('Access-Token', self.access_token)
        try:
            # send request to pushbullet api
            request.urlopen(req)
        except error.HTTPError as err:
            # pushbullet api return error
            print(err)
            raise
        except error.URLError:
            print("invalid url")
            raise

    def getDevices(self):
        req = request.Request(self.device_url)
        req.add_header('Access-Token', self.access_token)
        resp = None
        try:    
            resp = request.urlopen(req)
        except error.HTTPError as err:
            print(err)
            raise
        except error.URLError:
            print("invalid url")
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