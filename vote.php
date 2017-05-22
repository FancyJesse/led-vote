<?php
	if(empty($_POST['user_id'])||empty($_POST['color_id'])){
		echo false;
		exit();
	}
	require_once('MySqlSessionHandler.php');
	$handler = new MySqlSessionHandler();
	$success = $handler->connect();
	if($success){
		$success = $handler->led_vote($_POST['user_id'], $_POST['color_id']);
	}
	echo $success;
?>
