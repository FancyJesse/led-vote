<?php
	if(empty($_POST['color_id'])){
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

	try{
		$userData = array('user_id'=>$_POST['user_id'], 'type'=>'led', 'data'=>$_POST['color_id']);
		$disconnect = array('user_id'=>$_POST['user_id'], 'type'=>'request', 'data'=>'disconnect');
		$host = 'localhost';
		$port = 1330;
		$fp = fsockopen($host, $port, $errno, $errstr, 1);
		fwrite($fp, json_encode($userData));
		fgets($fp, 128);
		fwrite($fp, json_encode($disconnect));
		fgets($fp, 128);
		fclose($fp);
	} catch(Exception $e){
	}

?>
