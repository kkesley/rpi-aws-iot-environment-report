from influxdb import InfluxDBClient, exceptions
import json
from datetime import datetime
class NotificationDB:
    def __init__(self):
        config = {} # config placeholder
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

    def checkTodayNotifications(self):
        try:
            # check notification count for today
            result = self.client.query('select count(device) from notification_history where time >  now() - 1d group by time(1d) order by time desc limit 1')
            for item in result.get_points("notification_history"):
                if(item["count"] > 0):
                    return False
            return True
        except (exceptions.InfluxDBClientError, exceptions.InfluxDBServerError) as err:
            print(err)
            raise

    def writeHistory(self, devices = [], temperature=None, device=None):
        if(len(devices) <= 0):
            return
        # map the devices into data points
        data = []
        for device in devices:
            data.append({
                "measurement": "notification_history",
                "tags": {
                    "device": device,
                    "region": "ap-southeast-2"
                },
                "time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                "fields": {
                    "device": device,
                    "temperature": temperature
                }
            })

        # write the data points to db
        try:
            self.client.write_points(data)
        except (exceptions.InfluxDBClientError, exceptions.InfluxDBServerError) as err:
            print(err)
            raise