from influxdb import InfluxDBClient, exceptions
import json
from datetime import datetime
class BluetoothDB:
    def __init__(self):
        config = {} # config placeholder
        self.devices = []
        # read the config file
        try:
            config_file = open('./config/influxdb.json')
            # parse the content into dictionary
            config = json.loads(config_file.read())
        except FileNotFoundError:
            print("file not found")
            raise
        try:
            # connect to influx db
            self.client = InfluxDBClient(config["host"], config["port"], config["username"], config["password"], config["database"])
        except KeyError:
            print("key error")
            raise
        except (exceptions.InfluxDBClientError, exceptions.InfluxDBServerError) as err:
            print(err)
            raise

    def readDevices(self):
        try:
            config_file = open('./config/devices.json')
            # parse the content into dictionary
            self.devices = json.loads(config_file.read())
            return self.devices
        except FileNotFoundError:
            print("file not found")
            raise

    def getHistory(self):
        try:
            # check all devices
            result = self.client.query('select device from bt_history where time >  now() - 1d  group by device order by time desc limit 1')
            devices = []
            for item in result.get_points("bt_history"):
                devices.append(item["device"])
            return devices
        except (exceptions.InfluxDBClientError, exceptions.InfluxDBServerError) as err:
            print(err)
            raise

    def writeHistory(self, devices = [], temperature=None, host=None):
        if(len(devices) <= 0):
            return
        # map the devices into data points
        data = []
        for device in devices:
            data.append({
                "measurement": "bt_history",
                "tags": {
                    "device": device,
                    "host": host,
                    "region": "ap-southeast-2"
                },
                "time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                "fields": {
                    "temperature": temperature,
                    "device": device
                }
            })

        # write the data points to db
        try:
            self.client.write_points(data)
        except (exceptions.InfluxDBClientError, exceptions.InfluxDBServerError) as err:
            print(err)
            raise