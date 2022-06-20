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
import configparser
import gettext
import locale
import logging
import os
import platform
import time

# third-party library
import gi
from gi.repository import GLib
gi.require_version('Notify', '0.7')
from gi.repository import Notify

# imports from current project
from BatteryMonitor.config import APP, CONFIG_FILE, ICONS, LOCALE_DIR, MESSAGES
from BatteryMonitor.BMonitor import BMonitor


# i18n
locale.bindtextdomain(APP, LOCALE_DIR)
gettext.bindtextdomain(APP, LOCALE_DIR)
gettext.textdomain(APP)
_ = gettext.gettext

# log
module_logger = logging.getLogger('BatteryMonitor.Notification')


class get_notification():
	"""Triggers notification on battery state changes.

	Triggers informative and effective notification on every change of battery state.
	"""
	
	if platform.python_version() >= '3.6':
		TEST_MODE: bool
		last_notification: str
		last_percentage: int
	
	def __init__(self, TEST_MODE: bool = False) -> None:
		# self.sound_file = ''
		module_logger.info("Initiating Notification.")
		try:
			self.monitor = BMonitor(TEST_MODE)
		except:
			pass
		self.config = configparser.ConfigParser()
		self.load_config()
		
		Notify.init(_("Battery Monitor"))
		self.last_state = ''
		self.last_percentage = 0
		self.last_notification = ''
		self.notifier = Notify.Notification()
	
	def other_notification(self, notiftype):
		"""
		Shows other notifications like battery present/absent, acpi not installed etc.
		"""
		message = MESSAGES[notiftype]
		head = message[0]
		body = message[1]
		icon = ICONS[notiftype]
		notification = self.notifier.new(head, body, icon)
		notification.set_urgency(Notify.Urgency.CRITICAL)
		if (notiftype == "null"):
			#ToDo: this is not necessary anymore. maybe remove later
			# if notification type is null do not show any notification
			# just initialize
			module_logger.debug("This is a null notification to initialize notifications.")
		else:
			try:
				notification.show()
				time.sleep(self.notification_stability)
				module_logger.debug("Closing notification with head '%s'", head)
				notification.close()
			except GLib.GError as e:
				# TODO fixing GLib.GError: g-dbus-error-quark blindly
				pass
	
	def load_config(self):
		try:
			self.config.read(CONFIG_FILE)
			try:
				self.show_success = self.config['user'].getboolean('show_success')
			except KeyError or ValueError:
				self.show_success = self.config['default'].getboolean('show_success')
			try:
				self.upper_threshold_warning = int(self.config['user']['upper_threshold_warning'])
			except KeyError or ValueError:
				self.upper_threshold_warning = int(self.config['default']['upper_threshold_warning'])
			try:
				self.first_custom_warning = int(self.config['user']['first_custom_warning'])
			except KeyError or ValueError:
				self.first_custom_warning = int(self.config['default']['first_custom_warning'])
			try:
				self.second_custom_warning = int(self.config['user']['second_custom_warning'])
			except KeyError or ValueError:
				self.second_custom_warning = int(self.config['default']['second_custom_warning'])
			try:
				self.third_custom_warning = int(self.config['user']['third_custom_warning'])
			except KeyError or ValueError:
				self.third_custom_warning = int(self.config['default']['third_custom_warning'])
			try:
				self.low_battery = int(self.config['user']['low_battery'])
			except KeyError or ValueError:
				self.low_battery = int(self.config['default']['low_battery'])
			try:
				self.critical_battery = int(self.config['user']['critical_battery'])
			except KeyError or ValueError:
				self.critical_battery = int(self.config['default']['critical_battery'])
			
			try:
				self.use_sound = self.config['user'].getboolean('use_sound')
			except KeyError or ValueError:
				self.use_sound = self.config['default'].getboolean('use_sound')
			try:
				self.sound_file = self.config['user']['sound_file']
			except KeyError or ValueError:
				self.sound_file = self.config['default']['sound_file']
			
			try:
				self.notification_stability = int(self.config['user']['notification_stability'])
			except KeyError or ValueError:
				self.notification_stability = int(self.config['default']['notification_stability'])
			try:
				self.notification_count = int(self.config['user']['notification_count'])
			except KeyError or ValueError:
				self.notification_count = int(self.config['default']['notification_count'])
			module_logger.info('All settings were successfully read from config file - %s', CONFIG_FILE)
		except:
			module_logger.warning('Config file is missing or not readable. Using default configurations.')
			self.show_success = True
			self.upper_threshold_warning = 90
			self.first_custom_warning = 70
			self.second_custom_warning = 55
			self.third_custom_warning = 40
			self.low_battery = 30
			self.critical_battery = 15
			self.use_sound = True
			self.sound_file = '/usr/share/sounds/freedesktop/stereo/dialog-warning.oga'
			self.notification_stability = 5
			self.notification_count = 3
			
			self.save_config()
	
	def save_config(self):
		'''
		save configuration on first run as default settings
		'''
		config_dir = os.path.dirname(CONFIG_FILE)
		if os.path.exists(config_dir):
			pass
		else:
			os.makedirs(config_dir)
		
		self.config['default'] = {
			'show_success': self.show_success,
			'upper_threshold_warning': self.upper_threshold_warning,
			'first_custom_warning': self.first_custom_warning,
			'second_custom_warning': self.second_custom_warning,
			'third_custom_warning': self.third_custom_warning,
			'low_battery': self.low_battery,
			'critical_battery': self.critical_battery,
			'use_sound': self.use_sound,
			'sound_file': self.sound_file,
			'notification_stability': self.notification_stability,
			'notification_count': self.notification_count
		}
		
		with open(CONFIG_FILE, 'w') as f:
			self.config.write(f)
			
		module_logger.info("Saved new configuartion file to %s", CONFIG_FILE)
	
	def show_notification(self, notiftype: str, battery_percentage: int,
						  remaining_time: str = None, _count: int = None) -> None:
		
		try:
			for i in range(_count):
				self.monitor.is_updated()
				info = self.monitor.get_processed_battery_info()
				state = info["state"]
				battery_percentage = int(info["percentage"].replace("%", ""))
				remaining_time = info.get("remaining")
				message = MESSAGES[notiftype]
				head = message[0]
				body = message[1].format(battery_percentage=battery_percentage,
										remaining_time=remaining_time)
				icon = ICONS[notiftype]
				if state != self.last_state:
					continue
				module_logger.info("Showing notification %d on %s with %s", (i+1), head, body)
				notification = self.notifier.new(head, body, icon)
				notification.show()
				if self.use_sound:
					module_logger.debug("Playing %s with notification." % self.sound_file)
					os.system('paplay %s' % self.sound_file)
				time.sleep(self.notification_stability)
		except GLib.GError as e:
			# fixing GLib.GError: g-dbus-error-quark blindly
			# To Do: investigate the main reason and make a fix
			pass
	
	def show_specific_notifications(self, monitor: BMonitor):
		"""Shows specific notifications depending on the changes of battery state.
		
		Shows Notification only while state or last notification changes. Notification will not be shown for each percentage change. Sometimes acpi returns remaining time like *discharging at zero rate - will never fully discharge* We will skip it.
		"""
		info = monitor.get_processed_battery_info()
		state = info["state"]
		percentage = int(info["percentage"].replace("%", ""))
		remaining = info.get("remaining")
		count = self.notification_count
		
		if (remaining != "discharging at zero rate - will never fully discharge"):
			if state == 'discharging':
				# Show specific notifications when battery starts discharging
				if (state != self.last_state):
					# show discharging notification only once
					self.last_state = state
					self.last_notification = "discharging"
					self.show_notification(notiftype="discharging",
										battery_percentage=percentage,
										remaining_time=remaining, _count=1)
					
				self.last_percentage = percentage
				if (percentage <= self.critical_battery and
					self.last_notification != "critical_battery"):
					# show critical_battery notification
					self.last_notification = "critical_battery"
					self.show_notification(notiftype="critical_battery",
										battery_percentage=percentage,
										remaining_time=remaining, _count=count)
					
					return "critical_battery"
				
				elif (percentage > self.critical_battery and
					  percentage <= self.low_battery and
					  self.last_notification != "low_battery"):
					# show low_battery notification
					self.last_notification = "low_battery"
					self.show_notification(notiftype="low_battery",
										battery_percentage=percentage,
										remaining_time=remaining, _count=count)
					
					return "low_battery"
				
				elif (percentage > self.low_battery and
					  percentage <= self.third_custom_warning and
					  self.last_notification != "third_custom_warning"):
					# show third_custom_warning notification
					self.last_notification = "third_custom_warning"
					self.show_notification(notiftype="third_custom_warning",
										battery_percentage=percentage,
										remaining_time=remaining, _count=count)
					
					return "third_custom_warning"
				
				elif (percentage > self.third_custom_warning and
					  percentage <= self.second_custom_warning and
					  self.last_notification != "second_custom_warning"):
					# show second_custom_warning notification
					self.last_notification = "second_custom_warning"
					self.show_notification(notiftype="second_custom_warning",
										battery_percentage=percentage,
										remaining_time=remaining, _count=count)
					
					return "second_custom_warning"
				
				elif (percentage > self.second_custom_warning and
					  percentage <= self.first_custom_warning and
					  self.last_notification != "first_custom_warning"):
					# show first_custom_warning notification
					self.last_notification = "first_custom_warning"
					self.show_notification(notiftype="first_custom_warning",
										battery_percentage=percentage,
										remaining_time=remaining, _count=count)
					
					return "first_custom_warning"
			
			elif state == 'charging':
				if (state != self.last_state):
					# show charging notification only once
					self.last_state = state
					self.last_notification = "charging"
					self.show_notification(notiftype="charging",
										battery_percentage=percentage,
										remaining_time=remaining, _count=1)
				
				if (percentage >= self.upper_threshold_warning and
					not any(self.last_notification in x for x in
					["full", "unknown", "upper_threshold_warning"])):
						# show upper_threshold_warning notification
						self.last_percentage = percentage
						self.last_notification = "upper_threshold_warning"
						self.show_notification(notiftype="upper_threshold_warning",
											battery_percentage=percentage,
											remaining_time=remaining, _count=count)
						
						return "upper_threshold_warning"
			
			else:
				"""
					if last notification = charging, so is charging now then, the preceding block will not work.
				"""
				if state != self.last_notification:
					self.last_notification = state
					self.last_state = state
					self.show_notification(notiftype=state,
										battery_percentage=percentage,
										remaining_time=remaining, _count=count)
					
					return state
	
	def __del__(self):
		self.notifier.close()
		Notify.uninit()
