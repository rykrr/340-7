#!/bin/python3

import RPi.GPIO as gpio
import signal
import time
import sys

gpio.setmode(gpio.BCM)
gpio.setup(15, gpio.OUT)

def close(signal, frame):
	s.close()
	gpio.cleanup()
	print('Goodbye')
	sys.exit(0)

signal.signal(signal.SIGINT, close)


# Set String
string = ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."

while True:
	for c in string:
		if c == '.':
			gpio.output(15, gpio.LOW)
			sleep(0.15)
		
		if c == ' ' or c == '/':
			gpio.output(15, gpio.LOW)
			sleep(0.15)
		
		if c == '-':
			gpio.output(15, gpio.HIGH)
			sleep(0.45)
	sleep(5)
