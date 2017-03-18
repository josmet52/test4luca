# test_ds18b20.py

from ds18b20 import DS18B20
import time

# initialise temperature sensors
sensorArray = DS18B20()
count=sensorArray.device_count()
   
print('Infinite loop. CTRL-C for break')
print('')
while True:
   i = 0
   while i < count:
      temperature,sensorId,mesureStatus = sensorArray.tempC(i)
      print('Sensor '+sensorId+' mesure '+str(temperature)+' C')
   time.sleep(1)         


