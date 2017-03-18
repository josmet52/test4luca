import RPi.GPIO as GPIO
import time
from time import sleep    

# test for GPIO BUTTON INPUT-OUTPUT

GPIO.setmode(GPIO.BCM)
btn_1 = 17
btn_2 = 27
btn_3 = 22
btn_test = btn_2

GPIO.setup(btn_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(btn_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(btn_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
print('Infinite loop. CTRL-C for break')
print('')
while True:
    print( \
        'GPIO'+str(btn_1)+'='+str(GPIO.input(btn_1))+' / '+ \
        'GPIO'+str(btn_2)+'='+str(GPIO.input(btn_2))+' / '+ \
        'GPIO'+str(btn_3)+'='+str(GPIO.input(btn_3)) \
        )
    time.sleep(1)         
    
GPIO.cleanup()
