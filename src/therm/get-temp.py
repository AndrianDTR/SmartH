#!/usr/bin/env python

import os
import sys
import getopt

import MySQLdb as mdb

#import 

class Therm:
	loadedModules = ['w1-gpio', 'w1-therm']
	dbCon = None

	def __init__(self, modules = None):
		self.dbCon = self.dbConnect('localhost', 'therm', 'therm', 'therm')
		#self.loadMissedModules()
		
		if modules:
			self.loadedModules = modules
			
	def dbConnect(self, host, db, user, passwd):
		print "Connect"
		conn = None
		try:
			conn = mdb.connect(host, user, passwd, db)
		except mdb.Error, e:
		    print "Error %d: %s" % (e.args[0], e.args[1])
		    sys.exit(1)
		    
		return conn
		
	def loadMissedModules(self):
		res, missed = self.checkModules(self.loadedModules)
		if not res:
			for module in missed:
				self.loadModule(module)
				
	def loadSettings(self, file):
		consts = {}
		with open('consts.py', 'r') as const_file:
			for line in const_file:
				data = line.split('=')
				
				if len(data) > 1:
					consts[data[0].strip()] = data[1].strip()

		return consts

	def checkModules(self, modules):
		print "checkModules"
		missed = []
		res = True
		with open("/proc/modules") as loadedModules:
			for module in modules:
				if not module in loadedModules:
					res = False
					missed.append(module)
		
		return res, missed
			
	def loadModule(self, module):
		print "Load module", module
		os.system("sudo modprobe {0}".format(module))
		
	def renewDevicesList(self):
		print "renewDevicesList"
		w1dev = []
		
		try:
			with open('/sys/bus/w1/devices/w1_bus_master1/w1_master_slaves', 'r') as sensors_file:
				w1dev = sensors_file.readlines()
		except IOError:
			print "1-wire GPIO not loaded."
		
		self.updateDbDevices(w1dev)
		
	def updateDbDevices(self, devices):
		print "Update DB devices list"
		for device in devices:
			devId = long(device.replace('-',''), 16)
			try:
				cur = self.dbCon.cursor()
				cur.execute("select Id from 1wDevices where Id={0}".format(devId))
				
				data = cur.fetchone()
				if not data:
					stat = "insert into `1wDevices`(`Id`, `Name`) values({0}, '{1}')".format(devId, device.strip())
					cur.execute(stat)
			except mdb.Error, e:
				print "Error %d: %s" % (e.args[0], e.args[1])
		
		self.dbCon.commit()
	
	def getDeviceTypes(self):
		print "Get device types"
		
		types = []
		try:
			cur = self.dbCon.cursor()
			cur.execute("select * from `DeviceTypes`")
			types = cur.fetchall()
		except mdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
	
		return types
			
	def getDevicesList(self):
		print "getDevicesList"
		
		devices = []
		try:
			cur = self.dbCon.cursor()
			cur.execute("select * from 1wDevices")
			devices = cur.fetchall()
		except mdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
			
		return devices

	def getSensorTemp(self, id):
		print "getSensorTemp"

	def setHeaterState(self, state):
		print "Set heater state"

	def run(self):
		print "Run..."
		table = self.getDevicesList()
		print table
		if table:
			for row in table:
				print row
		
	
def main(argv):
	therm = Therm()
	print "main"
	
	try:
		opts, args = getopt.getopt(argv[1:],"hr",["nenew-sensor-list"])
	except getopt.GetoptError:
		print 'get-temp.py -r '
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'test.py -r'
			sys.exit()
		elif opt in ("-r", "--renew-sensor-list"):
			print "Renew sensors"
			therm.renewDevicesList()
	
	therm.run()

if __name__ == '__main__':
	main(sys.argv)

