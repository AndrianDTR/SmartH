
from error import *
from db import *

class Device:
	__types = [0x28, 0x2e]
	__directions = ['In', 'Out', 'Both']
	type = None
	direction = None
	value = None
	name = None
	id = None
	devModel = None
	
	params = {'name':name, 'id':id, 'type':type, 'direction':direction}
	
	def __init__(self, **kwargs):
		for key in kwargs.keys():
			if key not in self.params:
				raise MyError("Error! Only 'name', 'id', 'type', 'direction' keyword arguments are supported.")
		
		self.id = kwargs.get('id')
		self.type = kwargs.get('type')
		self.direction = kwargs.get('direction', self.__directions[0])
		self.name = kwargs.get('name', "{0}-{1}".format(self.type, self.id))
		
		if not self.id:
			raise MyError("Error! Device ID must be specified.")
		
		if not self.type:
			raise MyError("Error! Device TYPE must be specified.")
			
		self.devModel = self.getDeviceObjType()
		
	def __repr__(self):
		return self.name
		
	def __getitem__(self, item):
		return self.params.get(item)
		
	def __setitem__(self, item, value):
		self[item] = value
	
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
		return self.devModel.getValue(self.id)
		
	def setValue(self, value):
		self.devModel.setValue(self.id, value)
	
	def getType(self):
		return self.type
	
	def setType(self, type):
		self.type = type
	
	def getDirection(self):
		return self.type
	
	def setDirection(self, direction):
		self.direction = direction
	
	def getTypes(self):
		return self.types
	
	def getDirections(self):
		return self.directions
	
