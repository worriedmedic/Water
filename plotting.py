import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import time, datetime
import traceback
import sys, os.path
import subprocess

td = '90D'
td1 = '48H'
line_width = 2
label_offset = 3
water_flowing = True


if True:
	data = pd.read_csv('/home/pi/data_log/neutralizer_flow.log', names = ["Date", "Time", "Flow Rate", "Curent Volume", "Total Volume",], dtype=str)
	data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
	data = data.drop(['Date', 'Time'], 1)
	data = data.set_index('Datetime')
	data = data.convert_objects(convert_numeric=True)
	data['Difference'] = data['Total Volume'].diff(1)
	total = data['Curent Volume'].sum()
	fig = plt.figure(figsize=(10, 8), dpi=100)
	myFmt = mdates.DateFormatter('%m-%d %H:%M')
	plt.style.use('bmh')
	plt.rcParams['axes.facecolor']='w'
	plt.plot_date(data.last(td).index, data['Total Volume'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][0], label='Total Volume (mL)')
	plt.text(data.index[-1:][0], data['Total Volume'][-1], data['Total Volume'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][0])
	plt.legend(loc=2, ncol=2, fontsize=8).set_visible(True)
	plt.title('Neutralizer Water Flow: Past %s, Total: %s' %(td, total))
	plt.xlabel('Time')
	plt.ylabel('Fluid (mL)')
	plt.grid(True)
	plt.tight_layout()
	fig.axes[0].get_xaxis().set_major_formatter(myFmt)
	fig.autofmt_xdate()
	fig.text(0.5, 0.5, 'Dover Water Neutralizer', fontsize=25, color='gray', ha='center', va='center', alpha=0.35)
	fig.savefig('/home/pi/data_log/water_plot.png', bbox_inches='tight')
	subprocess.call(["sudo", "chmod", "+x", "/home/pi/data_log/water_plot.png"])
	subprocess.call(["sudo", "cp", "/home/pi/data_log/water_plot.png", "/var/www/html/"])
	if water_flowing:
		fig = plt.figure(figsize=(10, 8), dpi=100)
		myFmt = mdates.DateFormatter('%m-%d %H:%M')
		plt.style.use('bmh')
		plt.rcParams['axes.facecolor']='w'
		plt.plot_date(data.last(td1).index, data['Curent Volume'].last(td1).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][0], label='Instantaneous Volume (mL)')
		plt.text(data.index[-1:][0], data['Curent Volume'][-1], data['Curent Volume'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][0])
		plt.legend(loc=2, ncol=2, fontsize=8).set_visible(True)
		plt.title('Instantaneous Neutralizer Water Flow: Past %s, Total: %s' %(td1, total))
		plt.xlabel('Time')
		plt.ylabel('Fluid (mL)')
		plt.grid(True)
		plt.tight_layout()
		fig.axes[0].get_xaxis().set_major_formatter(myFmt)
		fig.autofmt_xdate()
		fig.text(0.5, 0.5, 'Dover Water Neutralizer', fontsize=25, color='gray', ha='center', va='center', alpha=0.35)
		fig.savefig('/home/pi/data_log/inst_water_plot.png', bbox_inches='tight')
		subprocess.call(["sudo", "chmod", "+x", "/home/pi/data_log/inst_water_plot.png"])
		subprocess.call(["sudo", "cp", "/home/pi/data_log/inst_water_plot.png", "/var/www/html/"])
