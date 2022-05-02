#!/usr/bin/python3

# Copyright: 2021-2022 Himadri Sekhar Basu <hsb10@iitbbs.ac.in>
#
# This file is part of battery-monitor.
#
# battery-monitor is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# battery-monitor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with battery-monitor. If not, see <http://www.gnu.org/licenses/>
# or write to the Free Software Foundation, Inc., 51 Franklin Street,
# Fifth Floor, Boston, MA 02110-1301, USA..
#
# Author: Himadri Sekhar Basu <hsb10@iitbbs.ac.in>
#

# standard library
import getpass
import glob
import logging
import setproctitle
import signal
import string
import sys
from random import choice

# third-party library
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# imports from current project
from AppIndicator import AppIndicator, bm_daemon

setproctitle.setproctitle("battery-monitor")

## Setup logging
def create_logfile():
	username = getpass.getuser()
	random_code =  ''.join(choice(string.digits) for _ in range(4))
	if len(glob.glob('/tmp/battery-monitor_'+username+'*')) ==0:
		logfile = '/tmp/battery-monitor_' + username + '_' + random_code + '.log'
	else:
		logfile = glob.glob('/tmp/battery-monitor_'+username+'*')[0]
	
	return logfile

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
logfile = create_logfile()
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
