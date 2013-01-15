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
		res, missed = checkModules(loadedModules)
		if not res:
			for module in missed:
				loadModule(module)
				
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
		
		
	"""
	$output = "";
	$attempts = 0;
	while ($output !~ /YES/g && $attempts < 5)
	{
		$output = `sudo cat /sys/bus/w1/devices/28-*/w1_slave 2>&1`;
		if($output =~ /No such file or directory/)
		{
			print "Could not find DS18B20\n";
			last;
		}
		elsif($output !~ /NO/g)
		{
			$output =~ /t=(\d+)/i;
			$temp = ($is_celsius) ? ($1 / 1000) : ($1 / 1000) * 9/5 + 32;
			$rrd = `/usr/bin/rrdtool update $dir/hometemp.rrd N:$temp:$outtemp`;
		}
	 
		$attempts++;
	}
	 
	#print "Inside temp: $temp\n";
	#print "Outside temp: $outtemp\n";
	"""


	def renewSensorsList(self):
		print "renewSensorsList"
		w1dev = []
		
		while True:
			try:
				with open('/sys/bus/w1/devices/w1_bus_master1/w1_master_slaves', 'r') as sensors_file:
					w1dev = sensors_file.readlines()
				break
			except IOError:
				loadMissedModules()
		
		self.updateDbSensors(w1dev)
		
	def updateDbSensors(self, sensors):
		print "Update DB sensors list"
		for sensor in sensors:
			sensor = long(sensor.replace('-',''), 16)
			print sensor
			cur = self.dbCon.cursor()
			cur.execute("select Id from 1wSensors where Id <> {0}".format(sensor))

			id = cur.fetchone()
			print id
		
	def getSensorsList(self):
		print "getSensorsList"

	def getSensorTemp(self, id):
		print "getSensorTemp"

	def setHeaterState(self, state):
		print "Set heater state"

	def run(self):
		print "Run..."
	
def main(argv):
	therm = Therm()
	print "main"
	
	try:
		opts, args = getopt.getopt(argv[1:],"hmr",["load-modules", "nenew-sensor-list"])
	except getopt.GetoptError:
		print 'get-temp.py -m|r '
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'test.py -m'
			sys.exit()
		elif opt in ("-m", "--load-modules"):
			print "Load modules"
			therm.loadMissedModules()
		elif opt in ("-r", "--renew-sensor-list"):
			print "Renew sensors"
			therm.renewSensorsList()
		else:
			run()

if __name__ == '__main__':
	main(sys.argv)

