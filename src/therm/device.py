
from error import *
from db import *

class Device:
	__types = []
	__directions = ['In', 'Out', 'Both']
	type = None
	direction = None
	value = None
	
	def getValue(self):
		return self.value
		
	def setValue(self, value):
		self.value = value
	
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
	
