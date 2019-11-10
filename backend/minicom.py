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

#fifo = open(FIFO, 'w')


# Setup Serial ##################################
#################################################

s = serial.Serial('/dev/ttyUSB1')


# Clean Exit ####################################
#################################################

def close(signal, frame):
	s.close()
	#fifo.close()
	
	print('Stream closed')
	sys.exit(0)

signal.signal(signal.SIGINT, close)


# Main Logic ####################################
#################################################

header = 'Digital: '
bits = []

while True:
	line = s.readline().decode('ascii')
        
        if not line.startswith(header):
            continue

        line = line[len(header):-1].strip()
	
        #print(morse.hex_to_bits([line]))
	(code, bits) = morse.decode(line, prev=bits, dot=3, dash=9, space=18)
	
