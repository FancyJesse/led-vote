<?php
	require_once('MySqlSessionHandler.php');
	$handler = new MySqlSessionHandler();
	$handler->connect();
	$handler->init_tables();
?>

