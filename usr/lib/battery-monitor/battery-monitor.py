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

## Setup logging
# Create logger
logger = logging.getLogger('Battery Monitor')
# Set logging level
logger.setLevel(logging.DEBUG)

# Create StreamHandler which logs even debug messages
cHandler = logging.StreamHandler()
# Set level for StreamHandler
cHandler.setLevel(logging.DEBUG)

# create file handler which logs only info messages
# Set the log filename
logfile = '/tmp/battery-monitor.log'
fHandler = logging.FileHandler(logfile)
# Set level for FileHandler
fHandler.setLevel(logging.INFO)

# create formatter and add it to the handlers
log_format = logging.Formatter('%(asctime)s %(name)s - %(levelname)s: %(message)s')
cHandler.setFormatter(log_format)
fHandler.setFormatter(log_format)

# add the handlers to the logger
logger.addHandler(cHandler)
logger.addHandler(fHandler)


def main() -> None:
	# checking Test Mode enabled or not
	try:
		if sys.argv[1] == '--test':
			TEST_MODE = True
		else:
			TEST_MODE = False
	except IndexError:
		TEST_MODE = False
	
	# initiaing app indicator
	logger.info("Battery Monitor Started.")
	AppIndicator()
	bm_daemon(TEST_MODE)
	Gtk.main()

if __name__ == '__main__':
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	main()
