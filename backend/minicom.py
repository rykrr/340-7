#!/bin/python3

import morse_decoder as morse
import serial
import signal
import json
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

fifo = open(FIFO, 'w')


# Setup Serial ##################################
#################################################

s = serial.Serial('/dev/ttyUSB1')


# Setup Cleanup on Exit #########################
#################################################

def close(signal, frame):
	s.close()
	fifo.close()
	print('Stream closed')
	sys.exit(0)

signal.signal(signal.SIGINT, close)


# Decode ########################################
#################################################

def decode(header, data, bits):
	data = data[len(header):-1].strip()
	prec = bits
	
	(code, bits) = morse.decode(data, prev=bits, dot=5, dash=15, space=30)
	(string, _) = code
	
	return (code, bits)


# Main Logic ####################################
#################################################

digital_header = 'Digital: '
digital_bits   = []

analog_header  = 'Analog: '
analog_bits    = []

_json = {'type': '', 'string': '', 'morse': ''}


while True:
	line = s.readline().decode('ascii')
	
	if line.startswith(digital_header):
		(output, digital_bits) = decode(digital_header, line, digital_bits)
		(stream, string) = output
		
		if len(string):
			_json['type']   = 'Digital'
			_json['string'] = string
			_json['morse']  = stream
			fifo.write(json.dumps(_json) + '\n')
			fifo.flush()
		continue
	
	if line.startswith(analog_header):
		(output, analog_bits) = decode(analog_header, line, analog_bits)
		(stream, string) = output
		
		if len(string):
			_json['type']   = 'Analog'
			_json['string'] = string
			_json['morse']  = stream
			fifo.write(json.dumps(_json) + '\n')
			fifo.flush()
		continue
