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
import gettext
import locale
import logging

# third-party library
import gi
gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# imports from current project
from BatteryMonitor.about_window import AboutWindow
from BatteryMonitor.bm_daemon import BMdaemon
from BatteryMonitor.config import APP, LOCALE_DIR
from BatteryMonitor.gui import run_BMwindow


# i18n
locale.bindtextdomain(APP, LOCALE_DIR)
gettext.bindtextdomain(APP, LOCALE_DIR)
gettext.textdomain(APP)
_ = gettext.gettext

# log
module_logger = logging.getLogger('BatteryMonitor.indicator')

class BMIndicator():
	"""Class for system tray icon.
	
	This class will show Battery Monitor icon in system tray.
	"""
	def __init__(self, TEST_MODE: bool = False):
		module_logger.debug("Initiaing Appindicator.")
		self.indicator = AppIndicator3.Indicator.new(APP, APP, AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
		self.indicator.set_title(_('Battery Monitor'))
		self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
		
		# run the daemon
		self.daemon = BMdaemon(TEST_MODE)
		
		# create menu
		self.indicator.set_menu(self.__create_menu())
		Gtk.main()
	
	def __create_menu(self):
		menu = Gtk.Menu()
		
		item_settings = Gtk.ImageMenuItem(_('Settings'))
		item_settings.set_image(Gtk.Image.new_from_icon_name("emblem-system-symbolic", Gtk.IconSize.MENU))
		item_settings.connect("activate", self.__settings_window)
		menu.append(item_settings)
		
		# Add "About" option in drop-down menu
		item_about = Gtk.ImageMenuItem(_('About'))
		item_about.set_image(Gtk.Image.new_from_icon_name("help-about-symbolic", Gtk.IconSize.MENU))
		item_about.connect("activate", self.open_about, Gtk.Window())
		menu.append(item_about)
		
		item_quit = Gtk.ImageMenuItem(_('Quit'))
		item_quit.set_image(Gtk.Image.new_from_icon_name("stock_close", Gtk.IconSize.MENU))
		item_quit.connect("activate", self.__quit)
		menu.append(item_quit)
		
		menu.show_all()
		
		return menu
	
	def __settings_window(self, *args):
		run_BMwindow()
	
	def open_about(self, signal, widget):
		about_window = AboutWindow(widget)
		about_window.show()
	
	def __quit(self, *args):
		Gtk.main_quit()
