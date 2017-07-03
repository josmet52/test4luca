#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import pyowm
from time import sleep
from ds18b20 import DS18B20
class HD44780:

    def __init__(self, pin_rs=7, pin_e=8, pins_db=[25, 24, 23, 15]):

        self.pin_rs=pin_rs
        self.pin_e=pin_e
        self.pins_db=pins_db

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_e, GPIO.OUT)
        GPIO.setup(self.pin_rs, GPIO.OUT)
        for pin in self.pins_db:
            GPIO.setup(pin, GPIO.OUT)

        self.clear()

    def clear(self):
        """ Blank / Reset LCD """

        self.cmd(0x33) # $33 8-bit mode
        self.cmd(0x32) # $32 8-bit mode
        self.cmd(0x28) # $28 8-bit mode
        self.cmd(0x0C) # $0C 8-bit mode
        self.cmd(0x06) # $06 8-bit mode
        self.cmd(0x01) # $01 8-bit mode

    def cmd(self, bits, char_mode=False):
        """ Send command to LCD """

        sleep(0.001)
        bits=bin(bits)[2:].zfill(8)

        GPIO.output(self.pin_rs, char_mode)

        for pin in self.pins_db:
            GPIO.output(pin, False)

        for i in range(4):
            if bits[i] == "1":
                GPIO.output(self.pins_db[::-1][i], True)

        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)

        for pin in self.pins_db:
            GPIO.output(pin, False)

        for i in range(4,8):
            if bits[i] == "1":
                GPIO.output(self.pins_db[::-1][i-4], True)


        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)

    def message(self, text):
        """ Send string to LCD. Newline wraps to second line"""

        for char in text:
            if char == '\n':
                self.cmd(0xC0) # next line
            else:
                self.cmd(ord(char),True)

if __name__ == '__main__':

    lcd = HD44780()
    sensorArray = DS18B20()
    count=sensorArray.device_count()
    btn_1 = 17
    btn_2 = 27
    btn_3 = 22

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(btn_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    vLoop = True
    while vLoop:
        i = 0
        
        while i < count:
            temperature,sensorId,mesureStatus = sensorArray.tempC(i)
            i = i + 1

        owm = pyowm.OWM('9820dafa77974dfdc5e1b0ff667d3079')  
        observation = owm.weather_at_place("Sion,ch")  
        weather = observation.get_weather()  

        fc = owm.daily_forecast('Sion,ch', limit=4)
        f = fc.get_forecast()
        index = 1

        for weather in f:
            date = weather.get_reference_time('iso')
            jour = date[8:10]
            mois = date [5:7]

            meteo = weather.get_status()
            if len(meteo) == 4:
                meteo = meteo + '  '
            if len(meteo) == 5:
                meteo = meteo + ' '

    
            temperature = str(weather.get_temperature('celsius'))
            lenString = len(temperature) - 6
            temp = temperature[lenString:lenString +5 ]

            if index == 1 :
                display1 = (jour+'-'+mois+' '+meteo+' '+temp)
            if index == 2 :
                display2 = (jour+'-'+mois+' '+meteo+' '+temp)
            if index == 3 :
                display3 = (jour+'-'+mois+' '+meteo+' '+temp)
            if index == 4 :
                display4 = (jour+'-'+mois+' '+meteo+' '+temp)

            index = index + 1

        lcd.clear()
        lcd.message(display1+'\n'+display2+'\n')
        print (display1+'\n'+display2+'\n')

        time.sleep(20)
        
        lcd.clear()
        lcd.message(display3+'\n'+display4+'\n')
        print (display3+'\n'+display4+'\n')

        vLoop = GPIO.input(btn_1) or GPIO.input(btn_2) or GPIO.input(btn_3)

        time.sleep(20)
            
    txtQuit = 'bye .. bacci a tuti!\n'
    print(txtQuit)
    lcd.message(txtQuit)
    GPIO.cleanup()

