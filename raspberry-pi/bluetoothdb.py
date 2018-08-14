from influxdb import InfluxDBClient, exceptions
class BluetoothDB:
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
            self.client = InfluxDBClient(config["host"], config["port"], config["username"], config["password"], "bluetooth_devices")
        except KeyError:
            print("key error")
            raise
        except (exceptions.InfluxDBClientError, exceptions.InfluxDBServerError) as err:
            print(err)
            raise

    def getDevices(self):
        try:
            # check notification count for today
            result = self.client.query('select device_mac, latest_notification from bluetooth_devices')
            devices = []
            for item in result.get_points("bluetooth_devices"):
                print(item["device_mac"] )
        except (exceptions.InfluxDBClientError, exceptions.InfluxDBServerError) as err:
            print(err)
            raise