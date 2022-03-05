#!/usr/bin/env python3

# standard library
import logging
import setproctitle
import signal
import sys

# third-party library
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# imports from current project
from AppIndicator import AppIndicator, bm_daemon

setproctitle.setproctitle("battery-monitor")


def main() -> None:

	## logging
	# Set the log format
	logging.basicConfig(level=logging.INFO)
	# Create logger
	logger = logging.getLogger('Battery Monitor')
	# Set logging level
	logger.setLevel(logging.DEBUG)
	# Set the log filename
	filename = '/tmp/battery-monitor.log'
	# Create formatters
	log_format = logging.Formatter('%(asctime)s: %(name)s - %(levelname)s: %(message)s')

	# Create StreamHandler object
	cHandler = logging.StreamHandler()
	# Set level for StreamHandler
	cHandler.setLevel(logging.DEBUG)
	#Add formatter to the handler
	cHandler.setFormatter(log_format)
	#Add StreanHandler object to logger
	logger.addHandler(cHandler)
	
	# checking Test Mode enabled or not
	try:
		if sys.argv[1] == '--test':
			TEST_MODE = True
		else:
			TEST_MODE = False
	except IndexError:
		TEST_MODE = False

	# initiaing app indicator
	AppIndicator()
	bm_daemon(TEST_MODE)
	Gtk.main()

if __name__ == '__main__':
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	main()
