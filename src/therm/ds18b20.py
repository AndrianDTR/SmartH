class DS18B20():
	__name = 'DS18B20'
	__type = 0x28
	
	def __str__(self):
		return self.__name
		
	def __repr__(self):
		return {'name':self.__name, 'code':self.__type}
		
	def getType(self):
		return self.__type
	
	def getName(self):
		return self.__name
	
	def getValue(self, id):
		pass
	
	def setValue(self, id, value):
		pass
