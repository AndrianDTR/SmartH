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
		self.loadMissedModules()
		
		if modules:
			self.loadedModules = modules
			
	def dbConnect(self, host, db, user, passwd):
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
		w1dev = []
		
		try:
			with open('/sys/bus/w1/devices/w1_bus_master1/w1_master_slaves', 'r') as sensors_file:
				w1dev = sensors_file.readlines()
		except IOError:
			print "1-wire GPIO not loaded."
		
		self.updateDbDevices(w1dev)
		
	def updateDbDevices(self, devices):
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
		types = []
		try:
			cur = self.dbCon.cursor()
			cur.execute("select * from `DeviceTypes`")
			for data in cur.fetchall():
				types = append({'Id':data[0], 'Name':data[1]})
		except mdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
	
		return types
			
	def getDevicesList(self):
		devices = []
		try:
			cur = self.dbCon.cursor()
			cur.execute("select `Id`,`Name`,`Type`,`Direction` from 1wDevices")
			for data in cur.fetchall():
				devices.append({'Id':data[0], 'Name':data[1], 'Type':data[2], 'Direction':data[3]})
		except mdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
			
		return devices

	def getDeviceValue(self, id):
		return self.getTemp(id)

	def getTemp(self, id):
		devId = hex(id)[2:][:-1]
		devId = devId[:2] + "-" + devId[2:]
		filename="/sys/bus/w1/devices/"+devId+"/w1_slave"
		temperature = 0
		try:
			with open(filename, 'r') as tfile:
				text = tfile.read()
				secondline = text.split("\n")[1]
				temperaturedata= secondline.split(" ")[9]
				temperature = float(temperaturedata[2:])
				temperature = temperature / 1000
		except IOError:
			print "Device read value error. Device ID:", devId
		
		return temperature

	def setDeviceValue(self, value):
		print "Set device value"

	def run(self):
		print "Run..."
		table = self.getDevicesList()
		if table:
			print table
			for row in table:
				print row['Name'], " = ", self.getDeviceValue(row['Id'])
				#print row
		
	
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

