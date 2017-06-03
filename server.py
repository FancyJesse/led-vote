from threading import Thread
import socket
import json
import time
import os

import config
import led


SERVER_HOSTNAME = ''
SERVER_SOCKET = None
CLIENT_LIST = []
START_TIME = None


def calc_uptime(start_time):
	days, rem = divmod(time.time() - start_time, 86400)
	hrs, rem = divmod(rem, 3600)
	mins, secs = divmod(rem, 60)
	up_time = '{:0>2}:{:0>2}:{:0>2}:{:05.2f}'.format(int(days), int(hrs), int(mins), secs)
	return str(up_time)


def send_all(sender, json_message):
	for client in CLIENT_LIST:
		if client != sender:
			client.send(json_message)


def client_handler(client):
	global CLIENT_LIST

	try:
		CLIENT_LIST.append(client)

		client_connected = True
		while client_connected:

			# receive message
			client_json = client.receive()
			print('RECV: {} - {}'.format(client.address, client_json))

			# json to send
			server_json = {}
			server_json['author'] = 'LED-Blink-Server'
			server_json['type'] = 'error'
			server_json['data'] = 'Server unable to handle request.'

			# request handler
			if client_json['type'] == 'request':
				if client_json['data'] == 'ledlist':
					server_json['type'] = 'ledlist'
					server_json['data'] = []
					for l in led.LED_LIST:
						server_json['data'].append(l.id)
				elif client_json['data'] == 'uptime':
					server_json['type'] = 'uptime'
					server_json['data'] = calc_uptime(START_TIME)
				elif client_json['data'] == 'disconnect':
					client_connected = False
					server_json['type'] = 'disconnect'
					server_json['data'] = True

			# message handler
			elif client_json['type'] == 'led':
				led_id = client_json['data']
				server_json['type'] = 'led'
				result = led.blink(led_id)
				server_json['data'] = result

			# invalid request
			else:
				print('Invalid Request {} - {}'.format(client.address, client_json))

			# send json to client
			client.send(server_json)

	except Exception as e:
		print('ERROR: {} - {}'.format(client.address, e))

	finally:
		client.disconnect()
		CLIENT_LIST.remove(client)


def start():
	global SERVER_SOCKET, SERVER_SOCKET, START_TIME

	SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	SERVER_HOSTNAME = socket.gethostname()

	# set IP Address based on OS type
	if(config.host == '?'):
		if(os.name == 'nt'):
			config.host = socket.gethostbyname(socket.getfqdn())
		elif(os.name == 'posix'):
			try:
				config.host = get_ip_address('eth0')
			except:
				config.host = get_ip_address('wlan0')
		else:
			raise Exception('Unable to start server - Unsupported OS')

	# attempt socket bind - exit after 10 fails
	attempt = 0
	while True:
		attempt += 1
		try:
			SERVER_SOCKET.bind((config.host, config.port))
			START_TIME = time.time()
			break
		except socket.error:
			if attempt == 10:
				raise Exception('Unable to connect socket after 10 attempts.')
			else:
				print('Error Connecting to {}:{} - Attempt {}'.format(config.host, config.port, attempt))
				time.sleep(10)


	print('Server Online - {}@{}:{}'.format(SERVER_HOSTNAME , config.host, config.port))
	SERVER_SOCKET.listen(5)

	# listen for clients - timeout:5mins
	while True:
		conn, addr = SERVER_SOCKET.accept()
		client = Client(conn, addr)
		Thread(target=client_handler, args=(client,)).start()


def stop():
	global SERVER_SOCKET
	SERVER_SOCKET.close()
	print('LED-Blink Server disconnected.')


# Unix system call
def get_ip_address(ifname):
	import fcntl
	import struct
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(
		s.fileno(),
		0x8915,  # SIOCGIFADOR
		struct.pack('256s', bytes(ifname[:15], 'utf-8'))
		)[20:24])


class Client:
	def __init__(self, conn, address):
		self.conn = conn
		self.address = address
		self.conn.settimeout(300)

	def send(self, json_data):
		json_data = json.dumps(json_data)
		self.conn.sendall((json_data + '\r\n').encode(encoding='utf_8', errors='strict'))
	def receive(self):
		data = self.conn.recv(1024).decode()
		message = json.loads(data)
		return message
	def disconnect(self):
		self.conn.close()


if __name__ == '__main__':
	try:
		led.setup()
		start()
	finally:
		stop()
		led.cleanup()
