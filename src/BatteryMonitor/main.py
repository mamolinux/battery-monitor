# Copyright (C) 2021-2022 Himadri Sekhar Basu <hsb10@iitbbs.ac.in>
#
# This file is part of theme-manager.
#
# theme-manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# theme-manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with theme-manager. If not, see <http://www.gnu.org/licenses/>
# or write to the Free Software Foundation, Inc., 51 Franklin Street,
# Fifth Floor, Boston, MA 02110-1301, USA..
#
# Author: Himadri Sekhar Basu <hsb10@iitbbs.ac.in>
#
import argparse
import gettext
import locale
import logging
from operator import truediv
import sys

from BatteryMonitor.config import APP, LOCALE_DIR, LOGFILE, __version__
from BatteryMonitor.indicator import BMIndicator
from BatteryMonitor.gui import run_BMwindow


# i18n
locale.bindtextdomain(APP, LOCALE_DIR)
gettext.bindtextdomain(APP, LOCALE_DIR)
gettext.textdomain(APP)
_ = gettext.gettext

description = 'A Python3-based GUI application to change different colour variants of GTK, Icon, Cursor and other themes.'

# Parse arguments
parser = argparse.ArgumentParser(prog=APP, description=description, conflict_handler='resolve')

parser.add_argument('-i', '--indicator', action='store_true', dest='start_indicator', default=False, help=("Start Battery Monitor Indicator"))
parser.add_argument('-t', '--test', action='store_true', dest='test_mode', default=False, help=("Test Battery Monitor by running indicator"))
parser.add_argument('-v', '--verbose', action='store_true', dest='show_debug', default=False, help=("Print debug messages to stdout i.e. terminal"))
parser.add_argument('-V', '--version', action='store_true', dest='show_version', default=False, help=("Show version and exit"))

args = parser.parse_args()

if args.show_version:
    print("%s: version %s" % (APP, __version__))
    sys.exit(0)

# Create logger
logger = logging.getLogger('BatteryMonitor')
# Set logging level
logger.setLevel(logging.DEBUG)
# create log formatter
log_format = logging.Formatter('%(asctime)s %(name)s - %(levelname)s: %(message)s')

# create file handler which logs only info messages
fHandler = logging.FileHandler(LOGFILE)
# Set level for FileHandler
fHandler.setLevel(logging.INFO)

# add formatter to the fHandler
fHandler.setFormatter(log_format)

# add the handler to the logger
logger.addHandler(fHandler)

if args.show_debug:
	# be verbose only when "-v[erbose]" is supplied
	# Create StreamHandler which logs even debug messages
	cHandler = logging.StreamHandler()
	# Set level for StreamHandler
	cHandler.setLevel(logging.DEBUG)
	
	# add formatter to the handler
	cHandler.setFormatter(log_format)

	# add the handler to the logger
	logger.addHandler(cHandler)

if args.test_mode:
	TEST_MODE = True
else:
	TEST_MODE = False

# module logger
module_logger = logging.getLogger('BatteryMonitor.main')

def start_BM ():
	if args.start_indicator:
		args.start_window = False
		# initiaing app indicator
		module_logger.debug("Initiaing Battery Monitor Indicator.")
		BMIndicator(TEST_MODE)
	else:
		args.start_window = True
	
	if args.start_window:
		# initiaing app window
		module_logger.debug("Initiaing Battery Monitor Window.")
		run_BMwindow()
