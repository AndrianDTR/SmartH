<?php
require "db.php";

$db_link = db_connect('localhost', 'therm', 'therm');
//db_query("SET character_set_results = 'utf8', character_set_client = 'utf8', character_set_connection = 'utf8', character_set_database = 'utf8', character_set_server = 'utf8'", $db_link);
db_select_db('therm');

$titles = array('titles'=>'"Time"');
$sensors = array();

$res = db_query("select Type, DeviceId, Name from `1wDevices`");
$cnt = 0;
while($u = db_fetch($res))
{
	$sensors[] = array('type'=>$u['Type'], 'id'=>$u['DeviceId']);
	$titles[$cnt] = '"'.$u['Name'].'"';
	$cnt++;
}

$cnt = count($sensors);
$cnt = 2;
$query = "select ";
$fields = "t1.TimeMark T, ";
$from = " from DeviceValues t1 ";

foreach($sensors as $sensor)
{
	$fields .= "IFNULL(t$cnt.Value, -100) V$cnt, ";
	$from .= "left join DeviceValues t$cnt on t$cnt.Type=".$sensor['type']." and t$cnt.Deviceid=".$sensor['id']." and t1.TimeMark=t$cnt.TimeMark ";
	$cnt++;
}

$prow = array();
$values = array();
$query .= substr($fields,0,-2).$from." where t1.TimeMark > TIMESTAMPADD(HOUR,-2,NOW()) group by t1.TimeMark";

echo($query);

$rcnt = 0;
$res = db_query($query);
while($u = db_fetch($res))
{

	$row = array();
	$cnt = 0;
	foreach($u as $field)
	{
		if($cnt == 0)
			$row[$cnt] = '"'.$field.'"';
		else
		{
			if($field != -100)
			{
				$prow[$cnt] = $field; 
				$row[$cnt] = round($field, 4);
			}	
			else
			{
				$row[$cnt] = round($prow[$cnt], 4);
			}
		}
		$cnt++;
	}
	
	$values[] = $row;
	$rcnt++;
}

echo("<BR>$rcnt");
/*
select t1.TimeMark T, IFNULL(t2.Value, -100) V2, IFNULL(t3.Value, -100) V3, IFNULL(t4.Value, -100) V4, IFNULL(t5.Value, -100) V5 from DeviceValues t1 left join DeviceValues t2 on t2.Type=40 and t2.Deviceid=74782089 and t1.TimeMark=t2.TimeMark left join DeviceValues t3 on t3.Type=40 and t3.Deviceid=74782090 and t1.TimeMark=t3.TimeMark left join DeviceValues t4 on t4.Type=40 and t4.Deviceid=74782091 and t1.TimeMark=t4.TimeMark left join DeviceValues t5 on t5.Type=40 and t5.Deviceid=74782092 and t1.TimeMark=t5.TimeMark group by t1.TimeMark
*/
?>

<html>
  <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([
<?php
		echo ("[".implode(", ", $titles)."],");
		foreach($values as $row)
		{
			echo ("[".implode(", ", $row)."],\n");
		}
?>
        ]);

        var options = {
          title: 'Company Performance'
        };

        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id="chart_div" style="width: 900px; height: 500px;"></div>
  </body>
</html>
<?php
//*/
?>
