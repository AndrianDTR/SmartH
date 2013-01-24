from error import MyError

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
	
	def isOk(self):
		return True
		
	def getValue(self, id):
		devId = hex(self.__type)[2:] + "-" + id
		filename="/sys/bus/w1/devices/"+devId+"/w1_slave"
		temperature = 9999
		try:
			with open(filename, 'r') as tfile:
				text = tfile.read()
				secondline = text.split("\n")[1]
				temperaturedata= secondline.split(" ")[9]
				temperature = float(temperaturedata[2:])
				temperature = temperature / 1000
		except IOError:
			print "Error! Reading device '{0}' was failed.".format(devId)
		
		return temperature
	
	def setValue(self, id, value):
		print "Set value for '{0}' is not supported".format(self.__name)
