import serial, io
import time
import datetime
import sys
import os.path
import traceback
import Adafruit_CharLCD as LCD

lcd = LCD.Adafruit_CharLCDPlate()
lcd.set_backlight(1)
baud = 9600
addr = '/dev/ttyACM0'
verbose = False
totaloutput = 0

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
ser.readline()

while True:
	now = time.strftime("%H:%M:%S")
	today = datetime.date.today()
	try:
		buffer = ser.readline()
		buffer = buffer.strip("\n")
		flowrate = buffer.split(',')[1]
		liquidflowing = buffer.split(',')[3]
		if totaloutput:
			oldoutput = totaloutput
		totaloutput = buffer.split(',')[5].strip('\r')
		if verbose:
			print("Current Flow Rate (mL/min): ", flowrate)
			print("Current Liquid Flowing (mL): ", liquidflowing)
			print("Total Liquid Output (mL): ", totaloutput)
		x = str(now) + ',' + flowrate + ',' + liquidflowing + ',' + totaloutput + '\n'
	except Exception:
		print("DATA ERROR", today, now, buffer)
		traceback.print_exc(file=sys.stdout)
		print('-' * 60)
	if totaloutput is not oldoutput:
		try:
			if not os.path.exists('data_log'):
				os.makedirs('data_log')
			fname = str(today) + '.log'  # log file to save data in
			fdirectory = './data_log/' + time.strftime("%Y-%m")
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
			message = "FR: " + flowrate + " LF: " + liquidflowing + "\n" +"Total: " + totaloutput
			lcd.clear()
			lcd.message(message)
		except Exception:
			print("LCD ERROR", today, now)
			traceback.print_exc(file=sys.stdout)
			print('-' * 60)
