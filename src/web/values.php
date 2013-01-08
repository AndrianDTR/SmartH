<?php
	$result = array();
	$content_file = '/sys/bus/w1/devices/w1_bus_master1/w1_master_slaves';

	$device_list = array();
	if(file_exists($content_file))
	{
		$content = file_get_contents($content_file);
		$device_list = explode('\n', $content);
	}
	
	foreach($device_list as $dev)
	{
		$value = "/sys/bus/w1/devices/$dev/w1_slave";
		$result[$dev] = $value;
	}
	return json_encode($result);
?>
