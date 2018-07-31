import os
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from sense_hat import SenseHat
import deviceid
import json
import time

# code supplied from http://yaab-arduino.blogspot.com/2016/08/accurate-temperature-reading-sensehat.html
# get CPU temperature
def get_cpu_temp():
  res = os.popen("vcgencmd measure_temp").readline()
  t = float(res.replace("temp=","").replace("'C\n",""))
  return(t)

# use moving average to smooth readings
def get_smooth(x):
  if not hasattr(get_smooth, "t"):
    get_smooth.t = [x,x,x]
  get_smooth.t[2] = get_smooth.t[1]
  get_smooth.t[1] = get_smooth.t[0]
  get_smooth.t[0] = x
  xs = (get_smooth.t[0]+get_smooth.t[1]+get_smooth.t[2])/3
  return(xs)

sense = SenseHat()
sense.clear()

t1 = sense.get_temperature_from_humidity()
t2 = sense.get_temperature_from_pressure()
t_cpu = get_cpu_temp()
t = (t1+t2)/2
t_corr = t - ((t_cpu-t)/1.5)
t_corr = get_smooth(t_corr)
humidity = sense.get_humidity()
pressure = sense.get_pressure()
data = {
    "deviceid": deviceid.getserial(),
    "humidity": humidity,
    "pressure": pressure,
    "temperature": t_corr,
    "timestamp": int(round(time.time() * 1000)),
}
dataStr = json.dumps(data)
print(dataStr)
myMQTTClient = AWSIoTMQTTClient("raspberry-RMIT")
myMQTTClient.configureEndpoint("a2jwan9azy4oaj.iot.ap-southeast-2.amazonaws.com", 8883)
myMQTTClient.configureCredentials("./root-ca.pem", "./f3ed0017cd-private.pem.key", "./f3ed0017cd-certificate.pem.crt")
myMQTTClient.connect()
myMQTTClient.publish("rmit", dataStr, 0)
myMQTTClient.disconnect()