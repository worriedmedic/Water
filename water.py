import serial, io
import time
import datetime
import sys
import os.path
import traceback
import pandas as pd
import numpy as np
import Adafruit_CharLCD as LCD
import subprocess

lcd = LCD.Adafruit_CharLCDPlate()
lcd.set_backlight(1)
baud = 9600
addr = '/dev/ttyACM0'
verbose = False
previous_zero = False
pre_liquidflowing = None
x = None

def txt_output():
	try:
		with open("./data_log/txt_output.txt", "w") as text_file:
			txt_now = datetime.datetime.now()
			text_file.write("Dover Lane well water neutralizer monitor, all values in mL.\n")
			text_file.write("Date: %s, Time: %s\n" %(txt_now.strftime('%Y-%m-%d'), txt_now.strftime('%H:%M:%S')))
			text_file.write("Flow Rate: %s, Liquid Flowing: %s\n" %(flowrate, liquidflowing))
			text_file.write("Total Output: %s | %s\n" %(totaloutput, sumtotal))
			
	except Exception:
		print("TXT OUTPUT ERROR", today, now, buffer)
		traceback.print_exc(file=sys.stdout)
		print('-' * 60)

for arg in sys.argv:
	if arg == "-v":
		verbose = True
	elif arg == "-h":
		print("Serial Monitoring Script - LWH 05/31/2017")
		print("For monitoring neutralizer output")
		print("-v VERBOSE")
		sys.exit()

#ser = serial.Serial(addr,9600)
#ser.readline()
#ser.readline()

try:
	data = pd.read_csv('/home/pi/data_log/neutralizer_flow.log', names = ["Date", "Time", "Flow Rate", "Curent Volume", "Total Volume",], dtype=str)
	data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
	data = data.drop(['Date', 'Time'], 1)
	data = data.set_index('Datetime')
	data = data.convert_objects(convert_numeric=True)
	total = data['Curent Volume'].sum()
except Exception:
	total = 0
	if verbose:
		print("NO LOG DETECTED... Setting Volume to 0ml")


for buffer in serial.Serial(addr, 9600):
	try:
		buffer = buffer.strip("\n")
		now = time.strftime("%H:%M:%S")
		today = datetime.date.today()
		if x:
			pre_x = x
			pre_flowrate = flowrate
			pre_liquidflowing = liquidflowing
			pre_totaloutput = totaloutput
		flowrate = buffer.split(',')[1]
		liquidflowing = buffer.split(',')[3]
		totaloutput = buffer.split(',')[5].strip('\r')
		sumtotal = float(total) + float(totaloutput)
		x = str(today) + ',' + str(now) + ',' + flowrate + ',' + liquidflowing + ',' + totaloutput + ',' + str(sumtotal) + '\n'
		if verbose:
			print("Current Flow Rate (mL/min): ", flowrate)
			print("Current Liquid Flowing (mL): ", liquidflowing)
			print("Total Liquid Output (mL): ", totaloutput, "|", sumtotal)
	except Exception:
		liquidflowing = 0
		print("DATA ERROR", today, now, buffer)
		traceback.print_exc(file=sys.stdout)
		print('-' * 60)
	if previous_zero is False or liquidflowing is not '0':
		txt_output()
		subprocess.call(["sudo", "chmod", "+x", "./data_log/txt_output.txt"])
		subprocess.call(["sudo", "cp", "./data_log/txt_output.txt", "/var/www/html/"])
		try:
			if not os.path.exists('data_log'):
				os.makedirs('data_log')
			fname = 'neutralizer_flow.log'  # log file to save data in
			fdirectory = './data_log/'
			fmode = 'a'  # log file mode = append
			if not os.path.exists(fdirectory):
				os.makedirs(fdirectory)
			outf = open(os.path.join(fdirectory, fname), fmode)
			if pre_liquidflowing is '0':
				outf.write(pre_x)
			outf.write(x)  # write line of text to file
			outf.flush()  # make sure it actually gets written out
		except Exception:
			print("DATA LOG ERROR", today, now, buffer)
			traceback.print_exc(file=sys.stdout)
			print('-' * 60)
		if liquidflowing is '0':
			previous_zero = True
		else:
			previous_zero = False
		try:
			message = str(today) + "," + str(now) + "\n" +"T:" + totaloutput + "|" + str(sumtotal)
			lcd.clear()
			lcd.message(message)
		except Exception:
			print("LCD ERROR", today, now)
			traceback.print_exc(file=sys.stdout)
			print('-' * 60)
