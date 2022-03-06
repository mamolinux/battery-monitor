#!/usr/bin/env python3

# standard library
import gettext
import locale
import subprocess
from threading import Thread
import time

# third-party library
import gi
gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

# imports from current project
from config import APPINDICATOR_ID
from config import ICONS
from AboutWindow import AboutWindow
from BatteryMonitor import BatteryMonitor
from Notification import get_notification
from SettingsWindow import bm_settings


# i18n
APP = 'battery-monitor'
LOCALE_DIR = "/usr/share/locale"
locale.bindtextdomain(APP, LOCALE_DIR)
gettext.bindtextdomain(APP, LOCALE_DIR)
gettext.textdomain(APP)
_ = gettext.gettext

class AppIndicator:
	"""Class for system tray icon.
	
	This class will show Battery Monitor icon in system tray.
	"""
	def __init__(self):
		self.indicator = AppIndicator3.Indicator.new(APPINDICATOR_ID, ICONS['app'], AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
		self.indicator.set_title(_('Battery Monitor'))
		self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
		
		# create menu
		self.indicator.set_menu(self.__create_menu())
	
	def __about_window(self, *args):
		about_window = AboutWindow()
		about_window.show()
	
	def __create_menu(self):
		menu = Gtk.Menu()
		
		item_settings = Gtk.MenuItem(_('Settings'))
		item_settings.connect("activate", self.__settings_window)
		menu.append(item_settings)
		
		item_about = Gtk.MenuItem(_('About'))
		item_about.connect("activate", self.__about_window)
		menu.append(item_about)
		
		item_quit = Gtk.MenuItem(_('Quit'))
		item_quit.connect("activate", self.__quit)
		menu.append(item_quit)
		menu.show_all()
		
		return menu
	
	def __settings_window(self, *args):
		settings = bm_settings("org.x.battery-monitor", Gio.ApplicationFlags.FLAGS_NONE)
		# settings.connect('destroy', Gtk.main_quit)
		# settings.show_all()
		# Gtk.main()
		settings.run()
	
	def __quit(self, *args):
		Gtk.main_quit()

class bm_daemon:
	
	def __init__(self, TEST_MODE: bool = False):
		# run the daemon
		self.daemon = Thread(target=self.__run_daemon, args=(TEST_MODE,))
		print(self.daemon.getName())
		# if 
		self.daemon.setDaemon(True)
		self.daemon.start()
	
	def __run_daemon(self, TEST_MODE: bool = False):
		# initiate notification with a null notification
		notification = get_notification("null")
		try:
			try:
				# initiaing BatteryMonitor
				monitor = BatteryMonitor(TEST_MODE)
			except subprocess.CalledProcessError as e:
				# show notification when acpi is not installed
				print("No acpi.")
				notification = get_notification("acpi")
				self.__quit()
				time.sleep(5)
		except IndexError as e:
			# show notification when battery is not present
			print("Where is my battery?")
			notification = get_notification("fail")
			self.__quit()
			time.sleep(5)
		
		# if battery is present execute the next lines
		# initiaing Notification
		print("OK, Battery present.")
		# check if success notification is shown
		if notification.success_shown in "yes":
			print("Success notifcation already shown.")
		else:
			print("Showing Success notification.")
			notification = get_notification("success")
		
		# this one shows wheter the battery is charging or discharging 
		# when the app starts
		notification.show_specific_notifications(monitor)
		while True:
			if monitor.is_updated():
				notification.show_specific_notifications(monitor)
			time.sleep(5)
		