#!/usr/bin/env python3
import json
import sys

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


def total_votes():
	return True, sqlitemanager.led_vote_count()


def top_users():
	return True, sqlitemanager.top_users()  # TODO


def register_user(username, secret):
	if sqlitemanager.user_register(username, secret):
		return True, 'Successfully Registered: {}'.format(username)
	else:
		return False, 'Failed to Register: {}'.format(username)


def user_stats(username=None):
	all_user_votes = sqlitemanager.user_data(username)
	if all_user_votes:
		return True, all_user_votes
	else:
		return False, all_user_votes


def rename_user(old_username, new_username):
	if sqlitemanager.user_rename(old_username, new_username):
		return True, 'Successfully Renamed: {} -> {}'.format(old_username, new_username)
	else:
		return False, 'Failed to Rename: {}'.format(old_username)

# Console commands
if __name__ == '__main__':
	args = sys.argv[1:]
	result = False, 'Invalid Arguments'
	if args:
		try:
			sqlitemanager.setup()
			if len(args) == 1:
				if args[0] == '-d':
					result = user_stats()
				elif args[0] == '-top':
					result = top_users()
				elif args[0] == '-votes':
					result = total_votes()
			elif len(args) == 2:
				if args[0] == '-stats':
					result = user_stats(args[1])
			elif len(args) == 3:
				if args[0] == '-register':
					result = register_user(args[1], args[2])
				elif args[0] == '-rename':
					result = rename_user(args[1], args[2])
		except Exception as e:
			result = False, str(e)
		finally:
			sqlitemanager.close()
		print(json.dumps({'success':result[0], 'data':result[1]}))
	else:
		main()
