from sense_hat import SenseHat
import os
import time

class Reading:
    def __init__(self):
        # initialize sense hat
        self.sense = SenseHat()
        self.sense.clear()
    
    def getReading(self):
        # get temperature from humidity
        t1 = self.sense.get_temperature_from_humidity()
        # get temperature from pressure
        t2 = self.sense.get_temperature_from_pressure()
        # get cpu temperature
        t_cpu = self.get_cpu_temp()
        # average temperature from humidity and pressure
        t = (t1+t2)/2
        # normalize temperature with cpu temperature
        t_corr = t - ((t_cpu-t)/1.5)
        # smooth the normalization by averaging
        t_corr = self.get_smooth(t_corr)

        # get humidity
        humidity = self.sense.get_humidity()
        # get pressure
        pressure = self.sense.get_pressure()

        # return data for pushing into iot
        return {
            "deviceid": self.getserial(),
            "humidity": humidity,
            "pressure": pressure,
            "temperature": t_corr,
            "timestamp": int(round(time.time() * 1000)),
        }

    # code supplied from http://yaab-arduino.blogspot.com/2016/08/accurate-temperature-reading-sensehat.html
    # get CPU temperature
    def get_cpu_temp(self):
        res = os.popen("vcgencmd measure_temp").readline()
        t = float(res.replace("temp=","").replace("'C\n",""))
        return(t)

    # code supplied from http://yaab-arduino.blogspot.com/2016/08/accurate-temperature-reading-sensehat.html
    # use moving average to smooth readings
    def get_smooth(self, x):
        smoothing = [x,x,x]
        smoothing[2] =smoothing[1]
        smoothing[1] = smoothing[0]
        smoothing[0] = x
        # average smoothing
        xs = (smoothing[0]+smoothing[1]+smoothing[2])/3
        return(xs)

    # code supplied from https://www.raspberrypi-spy.co.uk/2012/09/getting-your-raspberry-pi-serial-number-using-python/
    def getserial(self):
        # Extract serial from cpuinfo file
        cpuserial = "0000000000000000"
        try:
            f = open('/proc/cpuinfo','r')
            for line in f:
                if line[0:6]=='Serial':
                    cpuserial = line[10:26]
            f.close()
        except:
            cpuserial = "ERROR000000000"
        
        return cpuserial