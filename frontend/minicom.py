#!/bin/python3

import serial
import signal
import sys

s = serial.Serial('/dev/ttyUSB1')

def close(signal, frame):
	s.close()
	print('Stream closed')
	sys.exit(0)

signal.signal(signal.SIGINT, close)

while True:
	print(s.readline().decode('ascii'))


