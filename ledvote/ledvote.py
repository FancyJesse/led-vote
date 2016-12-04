import os

from logger import log
import config
import ledmanager
import server
import sqlitemanager


def setup():
	try:
		if config.LOG_DISPLAY:
			print('DISPLAY MODE IS ON - ALL LOG DATA WILL BE DISPLAYED ON CONSOLE')

		# Directory check
		if config.DIR_LOG == None:
			config.DIR_LOG = os.path.expanduser('~') + '/led-vote/log/'
		if config.DIR_DATABASE == None:
			config.DIR_DATABASE = os.path.expanduser('~') + '/led-vote/database/'
		if not os.path.exists(config.DIR_LOG):
			os.makedirs(config.DIR_LOG)
		if not os.path.exists(config.DIR_DATABASE):
			os.makedirs(config.DIR_DATABASE)
		log(__name__, 'Directory Check Complete')

		# Setup database
		sqlitemanager.setup()

		# Setup GPIO/LEDs
		ledmanager.setup()

		# Setup Server
		server.setup()
	except Exception as e:
		log(__name__, 'Something Went Wrong During Setup - {}'.format(e))
		exit()


def main():
	try:
		if config.LOG_DISPLAY:
			print('DEBUG MODE IS ON - ALL LOG DATA WILL BE DISPLAYED ON CONSOLE')
		setup()
		server.start()
	except Exception as e:
		log(__name__, 'Something Went Wrong - {}'.format(e))
	finally:
		log(__name__, 'LED-Vote Preparing to Exit ...')
		server.stop()
		ledmanager.cleanup()
		sqlitemanager.close()
		log(__name__, 'Good Bye.')


if __name__ == "__main__":
	main()
