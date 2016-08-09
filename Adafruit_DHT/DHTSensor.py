from .common import DHT11, DHT22, AM2302, read, read_retry
import time

from FlowerPlatformRuntime.ValueChangedEvent import ValueChangedEvent
import RPi.GPIO as GPIO

class DHTSensor:

    contributesToState = False
    
    onTemperatureChanged = None

    onHumidityChanged = None
    
    pin = -1
    
    pollInterval = 1000  # 1 second
    
    """    
    documentation of setup method
    """ 
    def setup(self) :
        self.lastTime = 0;
        self.lastHumidity = -1000;
        self.lastTemperature = -1000;
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

    def loop(self) :
        if time.time() * 1000 < self.lastTime + self.pollInterval : 
            return
      
        humidity, temperature = read_retry(DHT11, self.pin)

        if (humidity != self.lastHumidity) and (self.onHumidityChanged != None) : 
            event = ValueChangedEvent
            event.previousValue = self.lastHumidity
            event.currentValue = humidity
            self.onHumidityChanged(event)

        if (temperature != self.lastTemperature) and (self.onTemperatureChanged != None) : 
            event = ValueChangedEvent
            event.previousValue = self.lastTemperature
            event.currentValue = temperature
            self.onTemperatureChanged(event)

        self.lastHumidity = humidity
        self.lastTemperature = temperature
        self.lastTime = time.time() * 1000
        
    def stop(self) :
        return
    
    def getStateAsJson(self, instanceName) :
        return '"{}_temperature":{},"{}_humidity":{}'.format(instanceName, self.lastTemperature, instanceName, self.lastHumidity)
