import sys
import pushbullet

# get reading from environment
reading = sysreader.getReading()

# exit the program if the temperature is more than 20
if(reading["temperature"] > 20):
    sys.exit(0)


# send push bullet notification. It's too cold!
try:
    pusher = pushbullet.PushBullet()
    pusher.pushNotification(reading["temperature"])
except KeyError:
    print("please check your configuration file")
except FileNotFoundError:
    print("config file not found")
except:
    print("Fail to call pushbullet API")