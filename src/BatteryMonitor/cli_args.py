# Copyright (C) 2021-2024 Himadri Sekhar Basu <hsb10@iitbbs.ac.in>
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
