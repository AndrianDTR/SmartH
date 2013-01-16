#!/usr/bin/env python

import sys
import time
from deviceList import *
from daemon import Daemon

class MyDaemon(Daemon):
	devices = DeviceList()
	
	def storeDeviceValues(self):
		devices = self.devices.getDeviceList()
		if devices:
			print devices
			for row in devices:
				if row['Direction'] == 'In':
					print row['Name'], " = ", self.getDeviceValue(row['Id'])
					print row
		
	def run(self):
		count = 0
		while True:
			if count == 0:
				self.storeDeviceValues()
			
			if count == 59:
				count = 0
			else:
				count += 1
			time.sleep(1)
	
	def refresh(self):
		self.devices.renewDeviceList()

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
