# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#  Battery Monitor – Maximize Your Battery Life.
#  Copyright (C) 2016–2020 Maksudur Rahman Maateen
#  Copyright (C) 2021–2025 Himadri Sekhar Basu
#  Licensed under GPLv3 or later (see <http://www.gnu.org/licenses/>)
# -----------------------------------------------------------------------------

import argparse
import gettext
import locale


# i18n
APP = "@appname@"
LOCALE_DIR = "@localedir@"
locale.bindtextdomain(APP, LOCALE_DIR)
gettext.bindtextdomain(APP, LOCALE_DIR)
gettext.textdomain(APP)
_ = gettext.gettext

description = _('A Python3-based GUI application to notify user about charging, discharging and not charging state of the laptop battery on Linux.')

def command_line_args():
	# Parse arguments
	parser = argparse.ArgumentParser(prog=APP, description=description, conflict_handler='resolve')
	
	parser.add_argument('-i', '--indicator', action='store_true', dest='start_indicator', default=False, help=_("Start Battery Monitor Indicator"))
	parser.add_argument('-t', '--test', action='store_true', dest='test_mode', default=False, help=_("Test Battery Monitor by running indicator"))
	parser.add_argument('-v', '--verbose', action='store_true', dest='show_debug', default=False, help=_("Print debug messages to stdout i.e. terminal"))
	parser.add_argument('-V', '--version', action='store_true', dest='show_version', default=False, help=_("Show version and exit"))
	
	return parser
