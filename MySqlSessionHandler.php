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

        public function user_info($username){
                $query = 'SELECT * From user WHERE username=?';
                $stmt = $this->DB_CONN->prepare($query);
                $stmt->bind_param('s', $username);
                $stmt->execute();
                return $stmt->get_result();
        }

        public function user_register($username, $secret){
                $user_info = $this->user_info($username)->fetch_array(MYSQL_ASSOC);
                if(!$user_info){
                        $query =
                                'INSERT INTO user (username, secret, date_created, last_login)
                                VALUES (?, ?, NOW(), NOW())';
                        $stmt = $this->DB_CONN->prepare($query);
                        $stmt->bind_param('ss', $username, password_hash($secret, PASSWORD_BCRYPT));
                        $stmt->execute();
                        $user_info = $this->user_info($username)->fetch_array(MYSQL_ASSOC);
                        unset($user_info['secret']);
                        return $user_info;
                }
                return false;
        }

        public function user_login($username, $secret){
                $user_info = $this->user_info($username)->fetch_array(MYSQL_ASSOC);
                if(password_verify($secret, $user_info['secret'])){
                        $query = 'UPDATE user SET last_login=NOW() WHERE username=?';
                        $stmt = $this->DB_CONN->prepare($query);
                        $stmt->bind_param('s', $username);
                        $stmt->execute();
                        unset($user_info['secret']);
                        return $user_info;
                }
                return false;
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
