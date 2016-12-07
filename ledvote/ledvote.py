from logger import log
import ledmanager
import server
import sqlitemanager


def main():
	try:
		sqlitemanager.setup()
		ledmanager.setup()
		server.setup()
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
