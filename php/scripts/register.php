<?php
	if(empty($_POST['username'])||empty($_POST['secret'])||empty($_POST['secret_verify'])){
		echo false;
		exit();
	}
	if($_POST['secret'] != $_POST['secret_verify']){
		echo false;
		exit();
	}
	require_once('MySqlSessionHandler.php');
	$handler = new MySqlSessionHandler();
	$res = $handler->connect();
	if($res){
		$res = $handler->user_register($_POST['username'], $_POST['secret']);
		if($res){
			$res = json_encode($res);
		}
	}
	echo $res;
?>
