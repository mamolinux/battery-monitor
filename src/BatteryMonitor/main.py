# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#  Battery Monitor – Maximize Your Battery Life.
#  Copyright (C) 2016–2020 Maksudur Rahman Maateen
#  Copyright (C) 2021–2025 Himadri Sekhar Basu
#  Licensed under GPLv3 or later (see <http://www.gnu.org/licenses/>)
# -----------------------------------------------------------------------------

import gettext
import locale
import logging
import setproctitle
import sys

# imports from current project
from BatteryMonitor.cli_args import APP, LOCALE_DIR, command_line_args
from BatteryMonitor.config import LOGFILE, __version__
from BatteryMonitor.indicator import BMIndicator
from BatteryMonitor.gui import run_BMwindow


# i18n
locale.bindtextdomain(APP, LOCALE_DIR)
gettext.bindtextdomain(APP, LOCALE_DIR)
gettext.textdomain(APP)
_ = gettext.gettext

setproctitle.setproctitle(APP)

# Create logger
logger = logging.getLogger('BatteryMonitor')
# Set logging level
logger.setLevel(logging.DEBUG)
# create log formatter
log_format = logging.Formatter('%(asctime)s %(name)s:%(lineno)d - %(levelname)s: %(message)s')

# create file handler which logs only info messages
fHandler = logging.FileHandler(LOGFILE)
# Set level for FileHandler
fHandler.setLevel(logging.INFO)

# add formatter to the fHandler
fHandler.setFormatter(log_format)

# add the handler to the logger
logger.addHandler(fHandler)

# module logger
module_logger = logging.getLogger('BatteryMonitor.main')

parser = command_line_args()
args = parser.parse_args()

if args.show_version:
    print("%s: version %s" % (APP, __version__))
    sys.exit(0)

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

def start_BM():
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
