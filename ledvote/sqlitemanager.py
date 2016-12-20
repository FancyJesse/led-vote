from threading import Lock
import os
import sqlite3

import bcrypt

from logger import log
import config


MUTEX = Lock()
DATABASE = None
CURSOR = None


def setup():
	global DATABASE, CURSOR

	MUTEX.acquire()
	try:
		if config.DIR_DATABASE == None:
			config.DIR_DATABASE = os.path.expanduser('~') + '/led-vote/database/'
		if not os.path.exists(config.DIR_DATABASE):
			os.makedirs(config.DIR_DATABASE)

		DATABASE = sqlite3.connect(config.DIR_DATABASE + 'LED-Vote.db', check_same_thread=False)
		CURSOR = DATABASE.cursor()
		CURSOR.execute('CREATE TABLE IF NOT EXISTS user ('
					'username TEXT PRIMARY KEY COLLATE NOCASE,'
					'secret TEXT NOT NULL,'
					'date_created INTEGER DEFAULT 0,'
					'login_count INTEGER DEFAULT 0,'
					'last_login INTEGER DEFAULT 0,'
					'note TEXT)'
					)
		# force add led_id columns
		for led_id in [i[1] for i in config.LED_INFO]:
			try:
				query = 'ALTER TABLE user ADD COLUMN {0} INTEGER DEFAULT 0'.format(led_id)
				CURSOR.execute(query)
			except:
				pass

		DATABASE.commit()
		log(__name__, 'Database Created/Connected')
	except:
		raise Exception('{} - Unable to Setup Database'.format(__name__))
	finally:
		MUTEX.release()


def close():
	global db
	MUTEX.acquire()
	try:
		DATABASE.commit()
		DATABASE.close()
	except:
		pass
	finally:
		MUTEX.release()
	log(__name__, 'Database Disconnected')


def username_available(username):
	query = 'SELECT 1 FROM user WHERE username=?'
	CURSOR.execute(query, (username,))
	exist = CURSOR.fetchone()
	return exist is None


def user_register(username, secret):
	success = False
	MUTEX.acquire()
	try:
		success = username_available(username)
		if success:
			h = bcrypt.hashpw(secret.encode(), bcrypt.gensalt())
			query = 'INSERT INTO user (username, secret, date_created) values (?, ?, DATETIME("now","localtime"))'
			CURSOR.execute(query, (username, h))
			DATABASE.commit()
	except:
		raise Exception('{} - Unable to Register User: {} '.format(__name__, username))
	finally:
		MUTEX.release()
	return success


def user_login(username, secret):
	success = False
	MUTEX.acquire()
	try:
		query = 'SELECT username, secret FROM user WHERE username=?'
		CURSOR.execute(query, (username,))
		storedData = CURSOR.fetchone()
		if storedData:
			h = storedData[1]
			success = bcrypt.hashpw(secret.encode(), h) == h
			if success:
				query = 'UPDATE user SET last_login=DATETIME("now","localtime"), login_count=login_count+1 WHERE username=?'
				CURSOR.execute(query, (username,))
				DATABASE.commit()
				success = storedData[0]
	except:
		raise Exception('{} - Unable to Login User: {} '.format(__name__, username))
	finally:
		MUTEX.release()
	return success


def user_note(username, note):
	success = False
	MUTEX.acquire()
	try:
		success = not username_available(username)
		if success:
			query = 'UPDATE user SET note=? WHERE username=?'
			CURSOR.execute(query, (note, username))
			DATABASE.commit()
	except:
		raise Exception('{} - Unable to Update User Note: {}|{} '.format(__name__, username, note))
	finally:
		MUTEX.release()
	return success


def user_vote(username, led_id):
	success = False
	MUTEX.acquire()
	try:
		success = not username_available(username)
		if success:
			query = 'UPDATE user SET {0}={0}+1 WHERE username=?'.format(led_id)
			CURSOR.execute(query, (username,))
			DATABASE.commit()
	except:
		raise Exception('{} - Unable to Update User Vote: {}|{} '.format(__name__, username, led_id))
	finally:
		MUTEX.release()
	return success


def user_data(username=None):
	user_vote_dict_list = []
	led_id_list = [i[1] for i in config.LED_INFO]
	query = 'Select username, note, {0} FROM user'.format(', '.join(led_id_list))
	MUTEX.acquire()
	try:
		if username:
			query = query + ' WHERE username=?'
			CURSOR.execute(query, (username,))
		else:
			CURSOR.execute(query)
		for user_info in CURSOR.fetchall():
			user_dict = {}
			user_dict['username'] = user_info[0]
			user_dict['note'] = user_info[1]
			for led_idx, led_id in enumerate(led_id_list, 2):
				user_dict[led_id] = user_info[led_idx]
			user_vote_dict_list.append(user_dict)
	except:
		raise Exception('{} - Unable to get User Data: {} '.format(__name__, username))
	finally:
		MUTEX.release()
	return user_vote_dict_list


def led_vote_count():
	led_vote_dict = {}
	MUTEX.acquire()
	try:
		for led_id in [i[1] for i in config.LED_INFO]:
			query = 'Select sum({0}) FROM user'.format(led_id)
			CURSOR.execute(query)
			vote_count = CURSOR.fetchone()[0]
			if vote_count == None:
				vote_count = 0
			led_vote_dict[led_id] = vote_count
	except:
		raise Exception('{} - Unable to get LED Vote Count'.format(__name__))
	finally:
		MUTEX.release()
	return led_vote_dict
