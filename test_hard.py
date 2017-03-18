#!/usr/bin/python

import RPi.GPIO as GPIO
import time
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
            
        txt1=sensorId+'='+str(temperature)+'\n'
        txt2 = 'btn1='+str(GPIO.input(btn_1))+'/'+'btn2='+str(GPIO.input(btn_2))+'/'+'btn3='+str(GPIO.input(btn_3))
        lcd.clear()
        lcd.message(txt1+txt2+'\n')
        print (txt1+txt2+'\n')
        
        vLoop = GPIO.input(btn_1) or GPIO.input(btn_2) or GPIO.input(btn_3)
            
    txtQuit = 'bye .. bacci a tuti!\n'
    print(txtQuit)
    lcd.message(txtQuit)
    GPIO.cleanup()

