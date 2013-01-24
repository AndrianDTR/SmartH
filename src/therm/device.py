
from error import *
from db import *

DIRECTION_IN = 'In'
DIRECTION_OUT = 'Out'
DIRECTION_BOTH = 'Both'


class Device:
	type = None
	name = None
	id = None
	devModel = None
	
	params = ['name', 'id', 'type']
	
	def __init__(self, **kwargs):
		for key in kwargs.keys():
			if key not in self.params:
				raise MyError("Error! Only 'name', 'id', 'type' keyword arguments are supported.")
		
		self.id = kwargs.get('id')
		self.type = kwargs.get('type')
		self.name = kwargs.get('name', "{0}-{1}".format(self.type, self.id))
		
		if not self.id:
			raise MyError("Error! Device ID must be specified.")
		
		if not self.type:
			raise MyError("Error! Device TYPE must be specified.")
			
		self.devModel = self.getDeviceObjType()
		
	def __str__(self):
		return self.name
	
	def __repr__(self):
		return {'type':self.type, 'id':self.id, 'name':self.name}
		
	def getDeviceObjType(self):
		db = DB()
		cur = db.execute("select `Name` from `DeviceTypes` where `Code`={0}".format(self.type))
				
		data = cur.fetchone()
		if not data:
			raise MyError('Error. Specified type is not registered')
			
		cls = data[0]
		mod = __import__(cls.lower(), fromlist=[cls])
		return getattr(mod, cls)()
		
	def getValue(self):
		devId = str(hex(self.id)[2:-1]).zfill(12)
		return self.devModel.getValue(devId)
		
	def setValue(self, value):
		self.devModel.setValue(self.id, value)
