import serial, io
import time
import datetime
import sys
import os.path
import traceback
import Adafruit_CharLCD as LCD
import subprocess

lcd = LCD.Adafruit_CharLCDPlate()
lcd.set_backlight(1)
baud = 9600
addr = '/dev/ttyACM0'
verbose = False

def txt_output():
	try:
		with open("./data_log/txt_output.txt", "w") as text_file:
			txt_now = datetime.datetime.now()
			text_file.write("Dover Lane well water neutralizer monitor, all values in mL.\n")
			text_file.write("Date: %s, Time: %s\n" %(txt_now.strftime('%Y-%m-%d'), txt_now.strftime('%H:%M:%S')))
			text_file.write("Flow Rate: %s, Liquid Flowing: %s\n" %(flowrate, liquidflowing))
			text_file.write("Total Output: %s\n" %totaloutput)
			subprocess.call(["sudo", "cp", "/home/pi/data_log/txt_output.txt", "/var/www/html/"])
			subprocess.call(["sudo", "chmod", "+x", "/var/www/html/txt_output.txt"])
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

ser = serial.Serial(addr,9600)
ser.readline()
ser.readline()
buffer = ser.readline()
buffer = buffer.strip("\n")
flowrate = buffer.split(',')[1]
liquidflowing = buffer.split(',')[3]
totaloutput = buffer.split(',')[5].strip('\r')
txt_output()

while True:
	try:
		now = time.strftime("%H:%M:%S")
		today = datetime.date.today()
		buffer = ser.readline()
		buffer = buffer.strip("\n")
		flowrate = buffer.split(',')[1]
		liquidflowing = buffer.split(',')[3]
		totaloutput = buffer.split(',')[5].strip('\r')
		x = str(today) + ',' + str(now) + ',' + flowrate + ',' + liquidflowing + ',' + totaloutput + '\n'
		if verbose:
			print("Current Flow Rate (mL/min): ", flowrate)
			print("Current Liquid Flowing (mL): ", liquidflowing)
			print("Total Liquid Output (mL): ", totaloutput)
	except Exception:
		print("DATA ERROR", today, now, buffer)
		traceback.print_exc(file=sys.stdout)
		print('-' * 60)
	if liquidflowing is not '0':
		txt_output()
		try:
			if not os.path.exists('data_log'):
				os.makedirs('data_log')
			fname = 'neutralizer_flow.log'  # log file to save data in
			fdirectory = './data_log/'
			fmode = 'a'  # log file mode = append
			if not os.path.exists(fdirectory):
				os.makedirs(fdirectory)
			outf = open(os.path.join(fdirectory, fname), fmode)
			outf.write(x)  # write line of text to file
			outf.flush()  # make sure it actually gets written out
		except Exception:
			print("DATA LOG ERROR", today, now, buffer)
			traceback.print_exc(file=sys.stdout)
			print('-' * 60)
		try:
			message = str(today) + "," + str(now) + "\n" +"Total: " + totaloutput
			lcd.clear()
			lcd.message(message)
		except Exception:
			print("LCD ERROR", today, now)
			traceback.print_exc(file=sys.stdout)
			print('-' * 60)
