<?php
	if(!isset($_POST['user_id'])){
		echo false;
		exit();
	}
	require_once('MySqlSessionHandler.php');
	$handler = new MySqlSessionHandler();
	$handler->connect();
		$res =  $handler->led_total_votes();
	$arr = array();
	while($row = $res->fetch_array(MYSQL_ASSOC)) {
		$arr[] = $row;
	}
	echo json_encode($arr);
?>
