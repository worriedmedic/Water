import serial, io
import time
import datetime
import sys
import os.path
import traceback

baud 		= 9600
addr 		= '/dev/ttyACM0'
verbose 	= False

for arg in sys.argv:
	if arg == "-v":
		verbose = True
	elif arg == "-h":
		print("Serial Monitoring Script - LWH 05/31/2017")
		print("For monitoring neutralizer output")
		print("-v VERBOSE")
		sys.exit()

while(1):
	try:
		now = time.strftime("%H:%M:%S")
		today = datetime.date.today()
		ser = serial.Serial(addr,9600)
		buffer = ser.readline()
		buffer = buffer.strip("\n")
		x = str(today) + ',' + str(now) + ',' + str(buffer) + '\n'
		if verbose:
			print(x)
		flowrate 	= buffer.split(',')[1]
		liquidflowing 	= buffer.split(',')[3]
		totaloutput 	= buffer.split(',')[5].strip('\r')
		if verbose:
			print("Current Flow Rate (mL/min): ", flowrate)
			print("Current Liquid Flowing (mL): ", liquidflowing)
			print("Total Liquid Output (mL): ", totaloutput)
		
	except:
		print("ERROR")
