
from error import MyError
from device import Device
from db import *

import glob

class DeviceList(Singleton):
	devices = []
	db = None
	
	def __init__(self):
		self.db = DB()
		self.getDevicesList()
	
	def refreshDeviceTypes(self):
		w1Types = []
		
		path = os.path.dirname(os.path.abspath(__file__))
		for py in [f[:-3] for f in os.listdir(path) if f.startswith('ds') and f.endswith('.py')]:
			cls = str(py).upper()
			mod = __import__(py, fromlist=[cls])
			obj = getattr(mod, cls)()
			w1Types.append(obj)
		
		self.updateDbDeviceTypes(w1Types)
	
	def updateDbDeviceTypes(self, types):
		for type in types:
			cur = self.db.execute("select `Code`, `Name` from `DeviceTypes` where `Code`={0}".format(type.getType()))
				
			data = cur.fetchone()
			if not data:
				stat = "insert into `DeviceTypes`(`Code`, `Name`) values({0}, '{1}')".format(type.getType(), type.getName())
				self.db.execute(stat)
		
		self.db.sync()
		
	def getTypes(self):
		types = []
		cur = self.db.execute("select `Code` from `DeviceTypes`")
		
		for row in cur.fetchall():
			types.append(row[0])
			
		return types

	def checkDeviceType(self, type):
		types = self.getTypes()
		if type in types:
			return True
		return False
		
	def renewDevicesList(self):
		w1dev = []
		
		try:
			with open('/sys/bus/w1/devices/w1_bus_master1/w1_master_slaves', 'r') as sensors_file:
				w1dev = sensors_file.readlines()
		except IOError:
			raise MyError("Error! 1-wire GPIO not loaded.")
		
		self.updateDbDevices(w1dev)
	
	def updateDbDevices(self, devices):
		for device in devices:
			(devType, devId) = device.split('-')
			devId = long(devId, 16)
			devType = long(devType, 16)
			if not self.checkDeviceType(devType):
				print "Error! Unknown device type '{0}'.".format(devType)
				continue
			
			cur = self.db.execute("select `Type`, `DeviceId` from `1wDevices` where `DeviceId`={0} and `Type`={1}".format(devId, devType))
				
			data = cur.fetchone()
			if not data:
				stat = "insert into `1wDevices`(`Type`, `DeviceId`, `Name`) values({0}, {1}, '{2}')".format(devType, devId, device.strip())
				self.db.execute(stat)
		
		self.db.sync()
		
	def getDevicesList(self):
		devices = []
		cur = self.db.execute("select `Type`,`DeviceId`,`Name`,`Direction` from `1wDevices`")
		for data in cur.fetchall():
			devId = str(hex(data[1])[2:-1]).zfill(12)
			dev = Device(type=data[0], id=devId, name=data[2], direction=data[3])
			devices.append(dev)
			self.devices = devices
		
		return self.devices
