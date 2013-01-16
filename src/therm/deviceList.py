
import device
from db import *

class DeviceList:
	devices = []
	db = None
	
	def __init__(self):
		self.db = DB()
		self.db.connect('localhost', 'therm', 'therm', 'therm')
		
		self.renewDevicesList()
		self.getDevicesList()
		
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
			(devType, devId) = device.split('-')
			devId = long(devId, 16)
			try:
				cur = self.db.execute("select Type,Id from 1wDevices where Id={0} and Type={1}".format(devId, devType))
				
				data = cur.fetchone()
				if not data:
					stat = "insert into `1wDevices`(`Type`, `Id`, `Name`) values({0}, {1}, '{2}')".format(devType, devId, device.strip())
					self.db.execute(stat)
			except Error as e:
				print e
		
		self.db.sync()
		
	def getDevicesList(self):
		self.devices = []
		try:
			cur = self.dbCon.cursor()
			cur.execute("select `Id`,`Name`,`Type`,`Direction` from 1wDevices")
			for data in cur.fetchall():
				devices.append({'Id':data[0], 'Name':data[1], 'Type':data[2], 'Direction':data[3]})
		except mdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
			
