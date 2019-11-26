"""
Demo Flask application to test the operation of Flask with socket.io

Aim is to create a webpage that is constantly updated with random numbers from a background python process.

30th May 2014

===================

Updated 13th April 2018

+ Upgraded code to Python 3
+ Used Python3 SocketIO implementation
+ Updated CDN Javascript and CSS sources

"""




# Start with a basic flask app webpage.
from flask import Flask, render_template, url_for, copy_current_request_context, jsonify, request

from select import poll, POLLIN

import time
import RPi.GPIO as GPIO
import atexit
import morse_decoder as morse

__author__ = 'gennaro'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

@app.route('/', methods=['POST', 'GET'])
def hello():
	if request.method == 'POST':
		morse_sent = request.form.get('text-sent')
		morse_code = morse.encode(morse_sent)
		
		timing = 0.1
		
		print(morse_code)
		for c in morse_code:
			GPIO.output(21, GPIO.HIGH)
			
			if c == '.':
				GPIO.output(21, GPIO.LOW)
				time.sleep(timing)
			
			if c == ' ' or c == '/':
				time.sleep(timing)
			
			if c == '-':
				GPIO.output(21, GPIO.LOW)
				time.sleep(timing * 3)
			
			GPIO.output(21, GPIO.HIGH)
			time.sleep(timing)
	return render_template('index.html')

@app.route('/grab_morse')
def grab_morse():
	with open('/tmp/morse.fifo', 'r') as f:
		p = poll()
		p.register(f, POLLIN)
		
		e = p.poll()
		l = []
		
		for _ in e:
			l.append(f.readline())
		
		return jsonify(result=l)
	
	return jsonify(result=[])


def onexit():
	GPIO.cleanup()

if __name__ == '__main__':
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(21, GPIO.OUT)
	GPIO.output(21, GPIO.HIGH)
	atexit.register(onexit)
	app.run(host='0.0.0.0')
