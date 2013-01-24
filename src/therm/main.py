#!/usr/bin/env python

import sys
import time
from error import MyError
from deviceList import *
from daemon import Daemon

class MyDaemon(Daemon):
	devices = None
	
	def storeDeviceValues(self):
		devList = self.devices.getDevicesList()
		if devList:
			for row in devList:
				print row, row.getValue()
			
			print
		
	def run(self):
		try:
			self.devices = DeviceList()
			self.devices.renewDevicesList()

			count = 0
			while True:
				if count == 0:
					self.storeDeviceValues()
				
				if count == 1:
					count = 0
				else:
					count += 1
				time.sleep(1)
		except MyError as e:
			print e
		except Exception as e:
			print e
			exit(1)
			
	def refresh(self):
		try:
			self.devices = DeviceList()
			self.devices.refreshDeviceTypes()
			self.devices.renewDevicesList()
		except MyError as e:
			print e
		
if __name__ == "__main__":
	daemon = MyDaemon('/tmp/thermd.pid', )
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		elif 'refresh' == sys.argv[1]:
			daemon.refresh()
		else:
			print "Unknown command.\nUsage: main.py start|stop|restart|refresh"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: {0} start|stop|restart|refresh".format(sys.argv[0])
		sys.exit(2)
