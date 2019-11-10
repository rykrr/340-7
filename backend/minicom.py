#!/bin/python3

import morse_decoder as morse
import serial
import signal
import sys
import os

FIFO='/tmp/morse.fifo'

# Setup IPC #####################################
#################################################

try:
	if os.path.exists(FIFO):
		os.remove(FIFO)
	os.mkfifo(FIFO)
except OSError:
	print('Failed to launch')
	exit(1)

fifo = open(FIFO, 'a')


# Setup Serial ##################################
#################################################

s = serial.Serial('/dev/ttyUSB1')


# Clean Exit ####################################
#################################################

def close(signal, frame):
	s.close()
	fifo.close()
	
	print('Stream closed')
	sys.exit(0)

signal.signal(signal.SIGINT, close)


# Main Logic ####################################
#################################################

bits = []

while True:
	line = s.readline().decode('ascii')
	
	(code, bits) = morse.decode(line, prev=bits)
	
	print(code)
