<?php
	$output = shell_exec('/srv/therm/create-graphs.sh');
	print $output;
?>
