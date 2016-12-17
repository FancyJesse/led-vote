from threading import Thread
import json
import os
import socket
import time

from logger import log
import config
import ledmanager
import sqlitemanager


TIME_STARTED = ''
SERVER_HOSTNAME = ''
SERVER_SOCKET = None
LISTENING = True


def setup():
	global TIME_STARTED, SERVER_SOCKET, SERVER_HOSTNAME

	try:
		SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		SERVER_HOSTNAME = socket.gethostname()

		# set IP Address based on OS type
		if(config.SERVER_ADDRESS == 'AUTO-FIND'):
			if(os.name == 'nt'):
				config.SERVER_ADDRESS = socket.gethostbyname(socket.getfqdn())
			elif(os.name == 'posix'):
				try:
					config.SERVER_ADDRESS = get_ip_address('eth0')
				except:
					config.SERVER_ADDRESS = get_ip_address('wlan0')
			else:
				raise Exception('{} - Unable to Start Server - Unsupported OS'.format(__name__))

		# attempt socket bind - exit after 10 fails
		attempt = 0
		while True:
			attempt += 1
			try:
				SERVER_SOCKET.bind((config.SERVER_ADDRESS, config.SERVER_PORT))
				TIME_STARTED = time.time()
				break
			except socket.error:
				if attempt == 10:
					raise Exception('{} - Unable to Connect Socket After 10 Attempts.'.format(__name__))
				else:
					log(__name__, 'Error Connecting to {}:{} - Attempt {}'.format(config.SERVER_ADDRESS, config.SERVER_PORT, attempt))
					time.sleep(10)
	except Exception as e:
		raise Exception('{} - {}'.format(__name__, e))


def stop():
	global SERVER_SOCKET
	SERVER_SOCKET.close()
	log(__name__, 'Server Disconnected')


def get_up_time():
	days, rem = divmod(time.time() - TIME_STARTED, 86400)
	hrs, rem = divmod(rem, 3600)
	mins, secs = divmod(rem, 60)
	up_time = '{:0>2}:{:0>2}:{:0>2}:{:05.2f}'.format(int(days), int(hrs), int(mins), secs)
	return str(up_time)


def client_handler(client_conn, client_addr):
	try:
		client_logged_in = False
		client_connected = True

		while client_connected:

			# receive message
			client_message = client_conn.recv(1024).decode()
			client_json = json.loads(client_message)
			client_json_type = client_json['type']
			client_json_data = client_json['data']

			# json to send
			server_json = {}
			server_json['author'] = 'LED-Vote--Server'
			server_json['success'] = False
			server_json['data'] = 'Server Unable to Handle Request'

			# system handler
			if client_json_type == 'system':
				if client_json_data == 'ping':
					server_json['success'] = True
					server_json['data'] = 'ping'
				elif client_json_data == 'up_time':
					server_json['success'] = True
					server_json['data'] = get_up_time()
				elif client_json_data == 'disconnect':
					client_connected = False
					server_json['success'] = True
					server_json['data'] = 'Successfully Disconnected'
				else:
					log(__name__, 'Invalid Request - {} - {}'.format(client_addr[0] , client_message))

			# led ladder handler
			elif client_json_type == 'led_ladder':
				all_led_votes = sqlitemanager.led_vote_count()
				if all_led_votes:
					server_json['success'] = True
					server_json['data'] = all_led_votes

			# user ladder handler
			elif client_json_type == 'user_ladder':
				all_user_votes = sqlitemanager.user_vote_count()
				if all_user_votes:
					server_json['success'] = True
					server_json['data'] = all_user_votes

			# login handler
			elif client_json_type == 'login':
				client_logged_in = sqlitemanager.login_user(client_json_data['username'], client_json_data['secret'])
				if client_logged_in:
					server_json['success'] = True
					server_json['data'] = client_logged_in
				else:
					server_json['data'] = 'Invalid Login - Check Username and Password'
				log(__name__, 'Login User - {} - username:{} - success:{}'.format(client_addr[0], client_json_data['username'], client_logged_in))

			# register handler
			elif client_json_type == 'register':
				success = sqlitemanager.register_user(client_json_data['username'], client_json_data['secret'])
				server_json['success'] = success
				if success:
					server_json['data'] = 'Registration Successful - Please Login'
				else:
					server_json['data'] = 'Registration Failed - Username might be taken'
				log(__name__, 'Register User - {} - username:{} - success:{}'.format(client_addr[0], client_json_data['username'], success))

			# led vote handler - must be logged in
			elif client_json_type == 'led':
				if client_logged_in:
					success = sqlitemanager.vote(client_logged_in, client_json_data['led_id'])
					server_json['success'] = success
					if success:
						Thread(target=ledmanager.blink, args=(client_json_data['led_id'],)).start()
						all_led_votes = sqlitemanager.led_vote_count()
						server_json['data'] = all_led_votes
					else:
						server_json['data'] = 'Unable to process vote - Please log out and log in again'
				else:
					server_json['data'] = 'You must be logged in to do that'

			# invalid request
			else:
				log(__name__, 'Invalid Request - {} - {}'.format(client_addr[0] , client_message))

			# send json to client
			client_conn.sendall((json.dumps(server_json) + '\r\n').encode(encoding='utf_8', errors='strict'))

	except Exception as e:
		log(__name__, 'ERROR: {} - {}'.format(client_addr[0], e))

	finally:
		client_conn.close()
		log(__name__, 'Client Connection Closed - {}'.format(client_addr[0]))


def start():
	global TIME_STARTED, SERVER_SOCKET, SERVER_HOSTNAME

	log(__name__, 'Server Online - {}@{}:{}'.format(SERVER_HOSTNAME , config.SERVER_ADDRESS, config.SERVER_PORT))
	SERVER_SOCKET.listen(5)

	# listen for clients - timeout:5mins
	while LISTENING:
		client_conn, client_addr = SERVER_SOCKET.accept()
		client_conn.settimeout(300)
		if LISTENING:
			log(__name__, 'Client Connection Accepted - {}'.format(client_addr[0]))
			Thread(target=client_handler, args=(client_conn, client_addr)).start()


# Unix system call
def get_ip_address(ifname):
	import fcntl
	import struct
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(
		s.fileno(),
		0x8915,  # SIOCGIFADOR
		# struct.pack( '256s', ifname[:15] ) # python2.7
		struct.pack('256s', bytes(ifname[:15], 'utf-8'))  # python3
		)[20:24])
