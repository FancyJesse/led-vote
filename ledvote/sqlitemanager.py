from threading import Lock
import sqlite3
import bcrypt

from logger import log
import config


MUTEX = Lock()
DATABASE = None
CURSOR = None


def setup():
	global DATABASE, CURSOR

	try:
		MUTEX.acquire()
		DATABASE = sqlite3.connect(config.DIR_DATABASE + 'LED-Vote.db', check_same_thread=False)
		CURSOR = DATABASE.cursor()
		CURSOR.execute('CREATE TABLE IF NOT EXISTS user ('
					'username TEXT PRIMARY KEY COLLATE NOCASE,'
					'secret TEXT NOT NULL,'
					'dateCreated INTEGER DEFAULT 0,'
					'loginCount INTEGER DEFAULT 0,'
					'lastLogin INTEGER DEFAULT 0,'
					'ledRed INTEGER DEFAULT 0,'
					'ledYellow INTEGER DEFAULT 0,'
					'note TEXT)'
					)
		log(__name__, 'Database Created/Connected')
	except:
		raise Exception('{} - Unable to Setup Database'.format(__name__))
	finally:
		MUTEX.release()


def close():
	global db
	MUTEX.acquire()
	DATABASE.commit()
	DATABASE.close()
	MUTEX.release()
	log(__name__, 'Database Disconnected')


def username_available(username):
	query = 'SELECT 1 FROM user WHERE username=?'
	CURSOR.execute(query, (username,))
	exist = CURSOR.fetchone()
	return exist is None


def register_user(username, secret):
	MUTEX.acquire()
	success = username_available(username)
	if success:
		h = bcrypt.hashpw(secret.encode(), bcrypt.gensalt())
		query = 'INSERT INTO user (username, secret, dateCreated) values (?, ?, DATETIME("now","localtime"))'
		CURSOR.execute(query, (username, h))
		DATABASE.commit()
	MUTEX.release()
	return success


def login_user(username, secret):
	success = False
	MUTEX.acquire()
	query = 'SELECT secret FROM user WHERE username=?'
	CURSOR.execute(query, (username,))
	storedSecret = CURSOR.fetchone()
	if storedSecret:
		h = storedSecret[0]
		success = bcrypt.hashpw(secret.encode(), h) == h
		if success:
			query = 'UPDATE user SET lastLogin=DATETIME("now","localtime"), loginCount=loginCount+1 WHERE username=?'
			CURSOR.execute(query, (username,))
			DATABASE.commit()
	MUTEX.release()
	return success


def vote(username, ledID):
	MUTEX.acquire()
	success = not username_available(username)
	if success:
		query = 'UPDATE user SET {0}={0}+1 WHERE username=?'.format(ledID)
		CURSOR.execute(query, (username,))
		DATABASE.commit()
	MUTEX.release()
	return success


def led_vote_count():
	query = 'Select sum(ledRed), sum(ledYellow) FROM user'
	MUTEX.acquire()
	CURSOR.execute(query)
	MUTEX.release()
	return CURSOR.fetchone()


def user_vote_count(username=None):
	query = 'Select username, ledRed, ledYellow FROM user'
	MUTEX.acquire()
	if username:
		query = query + ' WHERE username=?'
		CURSOR.execute(query, (username,))
	else:
		CURSOR.execute(query)
	MUTEX.release()
	return CURSOR.fetchone() if username else CURSOR.fetchall()
