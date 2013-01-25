#!/usr/bin/env python

import sys
import time
from error import MyError
from deviceList import *
from device import DIRECTION_IN, DIRECTION_OUT, DIRECTION_BOTH
from daemon import Daemon

class MyDaemon(Daemon):
	devices = None
	"""
	pidfile = None
	stdin = None
	stdout = None
	stderr = None
	#"""
	def __init__(self, pidfile):
		Daemon.__init__(self, pidfile, )
		db = DB()
		db.connect('localhost', 'therm', 'therm', 'therm')
	
	def setDeviceStates(self):
		db = DB()
		devList = self.devices.getDevicesList(DIRECTION_OUT)
		
		for row in devList:
			print str(row)
			#stat = "insert into `DeviceValues`(`Type`, `DeviceId`, `Value`) values({0}, {1}, {2})".format(row.type, row.id, row.getValue())
			#db.execute(stat)
		#db.sync()
		#"""		
		
	def storeDeviceValues(self):
		db = DB()
		devList = self.devices.getDevicesList(DIRECTION_IN)
		
		for row in devList:
			stat = "insert into `DeviceValues`(`Type`, `DeviceId`, `Value`) values({0}, {1}, {2})".format(row.type, row.id, row.getValue())
			#print str(row), row.getValue()
			db.execute(stat)
		db.sync()
		
	def run(self):
		try:
			self.refresh()

			count = 0
			while True:
				try:
					if count == 0:
						self.storeDeviceValues()
						pass
				except MyError as e:
					print e
				
				if count == 59:
					count = 0
				else:
					count += 1
				
				self.setDeviceStates()
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
