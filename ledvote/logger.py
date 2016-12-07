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

	if config.DIR_LOG == None:
		config.DIR_LOG = os.path.expanduser('~') + '/led-vote/log/'
	if not os.path.exists(config.DIR_LOG):
		os.makedirs(config.DIR_LOG)

	if not os.path.exists(config.DIR_LOG + LOG_NAME):
		with open(config.DIR_LOG + LOG_NAME, 'w') as f:
			f.write('{} created on {}\n\n'.format(LOG_NAME, today.strftime('%B %d, %Y')))


def log(caller, msg):
	global LOG_NAME

	MUTEX.acquire()
	try:
		check_date()
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
	finally:
		MUTEX.release()


def check_date():
	global LOG_NAME
	if LOG_NAME != str(datetime.datetime.today().strftime('log_%Y%m%d.txt')):
		init()
