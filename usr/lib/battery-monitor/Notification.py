#!/usr/bin/env python3

# standard library
import configparser
import gettext
import locale
import os
import platform
import time

# third-party library
import gi
from gi.repository import GLib
gi.require_version('Notify', '0.7')
from gi.repository import Notify

# imports from current project
from BatteryMonitor import BatteryMonitor
from config import CONFIG_FILE
from config import ICONS
from config import MESSAGES


# i18n
APP = 'battery-monitor'
LOCALE_DIR = "/usr/share/locale"
locale.bindtextdomain(APP, LOCALE_DIR)
gettext.bindtextdomain(APP, LOCALE_DIR)
gettext.textdomain(APP)
_ = gettext.gettext


class get_notification():
	"""Triggers notification on battery state changes.

	Triggers informative and effective notification on every change of battery state.
	"""
	
	if platform.python_version() >= '3.6':
		TEST_MODE: bool
		last_notification: str
		last_percentage: int
	
	def __init__(self, notiftype: str, TEST_MODE: bool = False) -> None:
		
		try:
			self.monitor = BatteryMonitor(TEST_MODE)
		except:
			pass
		self.config = configparser.ConfigParser()
		self.load_config()
		
		Notify.init(_("Battery Monitor"))
		message = MESSAGES[notiftype]
		head = message[0]
		body = message[1]
		icon = ICONS[notiftype]
		self.last_state = ''
		self.last_percentage = 0
		self.last_notification = ''
		self.notifier = Notify.Notification()
		self.notification = self.notifier.new(head, body, icon)
		self.notification.set_urgency(Notify.Urgency.CRITICAL)
		
		if (notiftype == "null"):
			# if notification type is null do not show any notification
			# just initialize
			print("This is a null notification to initialize notifications.")
		else:
			if (notiftype != "success"):
				try:
					self.notification.show()
					time.sleep(self.notification_stability)
				except GLib.GError as e:
					# fixing GLib.GError: g-dbus-error-quark blindly
					pass
			else:
				self.notification.show()
				time.sleep(self.notification_stability)
			self.notification.close()
	
	def load_config(self):
		try:
			self.config.read(CONFIG_FILE)
			try:
				self.show_success = self.config['settings'].getboolean('show_success')
			except ValueError:
				self.show_success = True
			try:
				self.upper_threshold_warning = int(self.config['settings']['upper_threshold_warning'])
			except ValueError:
				self.upper_threshold_warning = 90
			try:
				self.first_custom_warning = int(self.config['settings']['first_custom_warning'])
			except ValueError:
				self.first_custom_warning = -1
			try:
				self.second_custom_warning = int(self.config['settings']['second_custom_warning'])
			except ValueError:
				self.second_custom_warning = -2
			try:
				self.third_custom_warning = int(self.config['settings']['third_custom_warning'])
			except ValueError:
				self.third_custom_warning = -3
			try:
				self.low_battery = int(self.config['settings']['low_battery'])
			except ValueError:
				self.low_battery = 30
			try:
				self.critical_battery = int(self.config['settings']['critical_battery'])
			except ValueError:
				self.critical_battery = 10
			try:
				self.use_sound = self.config['settings'].getboolean('use_sound')
			except ValueError:
				self.use_sound = True
			try:
				self.notification_stability = int(self.config['settings']['notification_stability'])
			except ValueError:
				self.notification_stability = 5
		except:
			module_logger.error('Config file is missing or not readable. Using default configurations.')
			self.show_success = True
			self.upper_threshold_warning = 90
			self.first_custom_warning = -1
			self.second_custom_warning = -2
			self.third_custom_warning = -3
			self.low_battery = 30
			self.critical_battery = 10
			self.use_sound = True
			self.notification_stability = 5
	
	def show_notification(self, notiftype: str, battery_percentage: int,
						  remaining_time: str = None, _count: int = None) -> None:
		
		message = MESSAGES[notiftype]
		head = message[0]
		body = message[1].format(battery_percentage=battery_percentage,
								 remaining_time=remaining_time)
		icon = ICONS[notiftype]
		try:
			for i in range(_count):
				if ("charging" or "discharging") in notiftype:
					notification = self.notifier.new(head, body, icon)
					notification.show()
					if self.use_sound:
						os.system("paplay /usr/share/sounds/Yaru/stereo/complete.oga")
				else:
					self.monitor.is_updated()
					info = self.monitor.get_processed_battery_info()
					state = info["state"]
					if state != self.last_state:
						continue
					notification = self.notifier.new(head, body, icon)
					notification.show()
					if self.use_sound:
						os.system("paplay /usr/share/sounds/Yaru/stereo/complete.oga")
					time.sleep(self.notification_stability)
				
		except GLib.GError as e:
			# fixing GLib.GError: g-dbus-error-quark blindly
			# To Do: investigate the main reason and make a fix
			pass
		# time.sleep(self.notification_stability)
		# self.notifier.close()
	
	def show_specific_notifications(self, monitor: BatteryMonitor):
		"""Shows specific notifications depending on the changes of battery state.
		
		Shows Notification only while state or last notification changes. Notification will not be shown for each percentage change. Sometimes acpi returns remaining time like *discharging at zero rate - will never fully discharge* We will skip it.
		"""
		info = monitor.get_processed_battery_info()
		state = info["state"]
		percentage = int(info["percentage"].replace("%", ""))
		remaining = info.get("remaining")
		
		count = 5
		
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
