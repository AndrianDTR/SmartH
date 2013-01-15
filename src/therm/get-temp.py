#!/usr/bin/env python

import os
import sys
import getopt

#import 

def loadSettings(file):
	consts = {}
	with open('consts.py', 'r') as const_file:
		for line in const_file:
			data = line.split('=')
			
			if len(data) > 1:
				consts[data[0].strip()] = data[1].strip()

	return consts

def checkModules(modules):
	print "checkModules"
	missed = []
	res = True
	with open("/proc/modules") as loadedModules:
		for module in modules:
			if not module in loadedModules:
				res = False
				missed.append(module)
	
	print "Res: ", res, missed
	return res, missed
		
def loadModule(module):
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

def getSensorTemp(id):
	print "getSensorTemp"

def getSensorsList():
	print "getSensorsList"

def setHeaterState(state):
	print "Set heater state"

def run():
	print "Run..."
	
def main(argv):
	print "main"
	
	try:
		opts, args = getopt.getopt(argv[1:],"hm",["load-modules"])
	except getopt.GetoptError:
		print 'get-temp.py -m '
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'test.py -m'
			sys.exit()
		elif opt in ("-m", "--load-modules"):
			print "Load modules"
			res, missed = checkModules(['w1-gpio', 'w1-therm'])
			if not res:
				for module in missed:
					loadModule(module)
		else:
			run()

if __name__ == '__main__':
	main(sys.argv)

