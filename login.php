<?php
	if(empty($_POST['username'])||empty($_POST['secret'])){
		echo false;
		exit();
	}
	require_once('MySqlSessionHandler.php');
	$handler = new MySqlSessionHandler();
	$res = $handler->connect();
	if($res){
		$res = $handler->user_login($_POST['username'], $_POST['secret']);
		if($res){
			$res = json_encode($res);
		}
	}
	echo $res;
?>
