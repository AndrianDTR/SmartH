<?php


	$result = array();
	$content_file = '/sys/bus/w1/devices/w1_bus_master1/w1_master_slaves';
	if(file_exists($content_file))
	{
		$content = file_get_contents($content_file);
		$result = explode('\n', $content);
	}
	return json_encode($result);
?>
