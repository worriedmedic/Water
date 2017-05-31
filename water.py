import RPi.GPIO as GPIO
import time
import datetime
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

counter = 0

try:
    while True:
        GPIO.wait_for_edge(4, GPIO.RISING)
        now = time.strftime("%H:%M:%S")
        today = datetime.date.today()
        counter = counter + 1
        print(today, now, counter)
        GPIO.wait_for_edge(4, GPIO.FALLING)
except exception:
    print("ERROR")
