#!/usr/bin/python3

# Copyright: 2016-2020 Maksudur Rahman Maateen <maateen@outlook.com>
#            2021-2022 Himadri Sekhar Basu <hsb10@iitbbs.ac.in>
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
# Author: Maksudur Rahman Maateen <maateen@outlook.com>
#

# standard library
import getpass
import gettext
import glob
import locale
import logging
import os
import string

from gi.repository import GObject
from random import choice
from threading import Thread


# i18n
APP = 'battery-monitor'
LOCALE_DIR = "/usr/share/locale"
locale.bindtextdomain(APP, LOCALE_DIR)
gettext.bindtextdomain(APP, LOCALE_DIR)
gettext.textdomain(APP)
_ = gettext.gettext

# Used as a decorator to run things in the background
def _async(func):
	def wrapper(*args, **kwargs):
		thread = Thread(target=func, args=args, kwargs=kwargs)
		thread.setDaemon(True)
		thread.start()
		return thread
	return wrapper

# Used as a decorator to run things in the main loop, from another thread
def idle(func):
	def wrapper(*args):
		GObject.idle_add(func, *args)
	return wrapper

## Setup logfile
def create_logfile():
	logpath = '/tmp/'
	dlimitter = '_'
	username = getpass.getuser()
	random_code =  ''.join(choice(string.digits) for _ in range(4))
	if len(glob.glob(logpath+APP+dlimitter+username+'*')) ==0:
		logfile = logpath + APP + dlimitter + username + dlimitter + random_code + '.log'
	else:
		logfile = glob.glob(logpath+APP+dlimitter+username+'*')[0]
	
	return logfile
# Set the log filename
LOGFILE = create_logfile()

# logger
module_logger = logging.getLogger('BatteryMonitor.config')

# get version
_path = os.path.dirname(os.path.abspath(__file__))
version_file = _path+'/VERSION'
__version__ = open(version_file, 'r').readlines()[0]


# Constants
CONFIG_DIR = os.path.expanduser('~/.config/'+APP+'/')
CONFIG_FILE = os.path.join(CONFIG_DIR+'config.cfg')
UI_PATH = _path+"/ui/"
_icon_path = _path + '/icons/'

ICONS = {
    "app": "tray-icon.svg",
    "success": "icon.png",
    "null": "icon.png",
    "fail": "icon.png",
    "acpi": "icon.png",
    "charging": "charging.png",
    "discharging": "discharging.png",
    "full":  "full-charge.png",
    "unknown":  "not-charging.png",
    "low_battery": "low-battery.png",
    "critical_battery": "critical-battery.png",
    "first_custom_warning": "discharging.png",
    "second_custom_warning": "discharging.png",
    "third_custom_warning": "discharging.png",
    "upper_threshold_warning": "charging.png"
}

for key in ICONS:
	ICONS[key] = _icon_path + ICONS[key]

MESSAGES = {
    "success": (
        _("Battery Monitor"),
        _("Cheers! Your battery is being monitored now.")
    ),
	
	"null": (
		_(""),
		_("")
	),

    "fail": (
        _("Battery Monitor"),
        _("Alas! Battery is not yet present!")
    ),

    "acpi": (
        _("Battery Monitor"),
        _("Dependency Error! acpi is not installed.")
    ),

    "charging": (
        _("Charging"),
        _("Now {battery_percentage} %, {remaining_time}")
    ),

    "discharging": (
        _("Discharging"),
        _("Now {battery_percentage} %, {remaining_time}")
    ),

    "full": (
        _("Fully Charged - Unplug your Charger"),
        _("{battery_percentage} % Remaining")
    ),

    "unknown": (
        _("Fully Charged"),
        _("{battery_percentage} % Remaining")
    ),

    "low_battery": (
        _("Low Battery"),
        _("Now {battery_percentage} %, {remaining_time}")
    ),

    "critical_battery": (
        _("Critically Low Battery"),
        _("Only {battery_percentage} %, {remaining_time}")
    ),

    "first_custom_warning": (
        _("First Custom Warning"),
        _("Now {battery_percentage} %, {remaining_time}")
    ),

    "second_custom_warning": (
        _("Second Custom Warning"),
        _("Now {battery_percentage} %, {remaining_time}")
    ),

    "third_custom_warning": (
        _("Third Custom Warning"),
        _("Now {battery_percentage} %, {remaining_time}")
    ),
    "upper_threshold_warning": (
        _("Upper Threshold Warning - Unplug your Charger"),
        _("Now {battery_percentage} %, {remaining_time}")
    )
}

TEST_CASES = {
    "state": [
        _("Full"),
        _("Charging"),
        _("Discharging")
    ],
    "remaining": [
        _("00:10:12 remaining"),
        _("01:47:31 remaining"),
        _("02:33:47 remaining"),
        _("03:24:25 remaining"),
        _("discharging at zero rate - will never fully discharge")
    ]
}
