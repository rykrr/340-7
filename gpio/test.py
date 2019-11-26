#!/bin/python3

import RPi.GPIO as gpio
import signal
import time
import sys

gpio.setmode(gpio.BCM)
gpio.setup(21, gpio.OUT)

def close(signal, frame):
    gpio.cleanup()
    print('Goodbye')
    sys.exit(0)

signal.signal(signal.SIGINT, close)


# Set String
string = ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."
timing = 0.1

while True:
	for c in string:
		gpio.output(21, gpio.HIGH)
	
	if c == '.':
		gpio.output(21, gpio.LOW)
		time.sleep(timing)
	
	if c == ' ' or c == '/':
		gpio.output(21, gpio.LOW)
		time.sleep(timing)
	
	if c == '-':
		time.sleep(timing * 3)
	gpio.output(21, gpio.HIGH)
	
	time.sleep(5)
