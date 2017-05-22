<?php
class MySqlSessionHandler{

	protected $DB_CONN;
	private $host = '';
	private $user = '';
	private $secret = '';
	private $schema = '';

	public function connect(){
		$this->DB_CONN = new mysqli($this->host, $this->user, $this->secret, $this->schema);
		return !$this->DB_CONN->connect_errno;
	}

	public function close(){
		return $this->DB_CONN->close();
	}

	public function led_total_votes(){
		$query = 'SELECT * FROM led';
		return $this->DB_CONN->query($query);
	}

	public function led_user_votes($user_id){
		$query = 'SELECT * FROM led WHERE user_id=?';
		$stmt = $this->DB_CONN->prepare($query);
		$stmt->bind_param('i', $user_id);
		$stmt->execute();
		return $stmt->get_result()->fetch_array(MYSQL_ASSOC);
	}

	public function led_vote($user_id, $color_id){
		if(!$this->led_user_votes($user_id)){
			$query = 'INSERT INTO led (user_id) VALUES (?)';
			$stmt = $this->DB_CONN->prepare($query);
			$stmt->bind_param('i', $user_id);
			$stmt->execute();
		}
		$query = 'UPDATE led SET ' . $color_id . '='. $color_id . '+1 WHERE user_id=?';
		$stmt = $this->DB_CONN->prepare($query);
		if($stmt && $stmt->bind_param('i', $user_id)){
			return $stmt->execute();
		}
		return false;
	}

}
?>
