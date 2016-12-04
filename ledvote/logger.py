from threading import Lock
import datetime
import os

import config


LOG_NAME = ''
MUTEX = Lock()

def init():
	global LOG_NAME

	today = datetime.datetime.today()
	LOG_NAME = str(today.strftime('log_%Y%m%d.txt'))

	if not os.path.exists(config.DIR_LOG + LOG_NAME):
		with open(config.DIR_LOG + LOG_NAME, 'w') as f:
			f.write('{} created on {}\n\n'.format(LOG_NAME, today.strftime('%B %d, %Y')))


def log(caller, msg):
	MUTEX.acquire()

	checkDate()
	global LOG_NAME

	try:
		with open(config.DIR_LOG + LOG_NAME, 'a') as f:
			formatedMessage = datetime.datetime.now().strftime(
				'%Y-%m-%d %H:%M:%S\t{}\t{}\n'.format('{:<15}'.format('[' + caller + ']'), msg))
			f.write(formatedMessage)
			if config.LOG_DISPLAY:
				print(formatedMessage)
	except:
		init()
		MUTEX.release()
		log(caller, msg)

	if MUTEX.locked():
		MUTEX.release()


def checkDate():
	global LOG_NAME

	if LOG_NAME != str(datetime.datetime.today().strftime('log_%Y%m%d.txt')):
		init()


def currentLog():
	if not os.path.isfile(config.DIR_LOG + LOG_NAME):
		return False
	return config.DIR_LOG + LOG_NAME
