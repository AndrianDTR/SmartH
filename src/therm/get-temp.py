#!/usr/bin/env python

import os
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

def main():
	print "main"
	res, missed = checkModules(['w1-gpio', 'w1-therm'])
	if not res:
		for module in missed:
			loadModule(module)

if __name__ == '__main__':
	main()

