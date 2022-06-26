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
import gettext
import locale
import logging
import subprocess
import time

# third-party library
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# imports from current project
from BatteryMonitor.config import APP, _async, LOCALE_DIR
from BatteryMonitor.BMonitor import BMonitor
from BatteryMonitor.Notification import get_notification


# i18n
locale.bindtextdomain(APP, LOCALE_DIR)
gettext.bindtextdomain(APP, LOCALE_DIR)
gettext.textdomain(APP)
_ = gettext.gettext

# log
module_logger = logging.getLogger('BatteryMonitor.bm_daemon')

class BMdaemon():
	
	def __init__(self, TEST_MODE: bool = False):
		module_logger.debug("Initiaing Battery Monitor daemon.")
		# run the daemon
		start_BMdaemon = _async(self.start_daemon)
		start_BMdaemon(TEST_MODE)
	
	def start_daemon(self, TEST_MODE: bool = False):
		# initiate notification
		notification = get_notification(TEST_MODE)
		try:
			# initiaing BatteryMonitor
			monitor = BMonitor(TEST_MODE)
		except subprocess.CalledProcessError as e:
			# show notification when acpi is not installed
			module_logger.error("Dependency Error! acpi is not installed.")
			notification = get_notification("acpi")
			Gtk.main_quit()
			time.sleep(5)
		except IndexError as e:
			# show notification when battery is not present
			module_logger.error("Alas! Battery is not yet present. Where is my battery?")
			notification = get_notification("fail")
			Gtk.main_quit()
			time.sleep(5)
		
		# if battery is present execute the next lines
		module_logger.info("OK, Battery present.")
		# check if 'success' notification will be shown
		if notification.show_success:
			module_logger.info("Showing 'Success' notification.")
			notification.other_notification("success")
		else:
			module_logger.info("Showing 'Success' notifcation disabled.")
		
		# this one shows whether the battery is charging or discharging 
		# when the app starts
		notification.show_specific_notifications(monitor)
		
		# start an infinite loop to monitor continuously
		while True:
			# load new settings if updated
			notification.load_config()
			
			if monitor.is_updated():
				notification.show_specific_notifications(monitor)
			time.sleep(5)
