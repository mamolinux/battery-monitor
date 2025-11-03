# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#  Battery Monitor – Maximize Your Battery Life.
#  Copyright (C) 2016–2020 Maksudur Rahman Maateen
#  Copyright (C) 2021–2025 Himadri Sekhar Basu
#  Licensed under GPLv3 or later (see <http://www.gnu.org/licenses/>)
# -----------------------------------------------------------------------------

# standard library
import configparser
import gettext
import locale
import logging
import os

# third-party library
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

# imports from current project
from BatteryMonitor.cli_args import APP, LOCALE_DIR
from BatteryMonitor.config import CONFIG_FILE, UI_PATH
from BatteryMonitor.about_window import AboutWindow
from BatteryMonitor.ErrorLib import ValidationError

# i18n
locale.bindtextdomain(APP, LOCALE_DIR)
gettext.bindtextdomain(APP, LOCALE_DIR)
gettext.textdomain(APP)
_ = gettext.gettext

# log
module_logger = logging.getLogger('BatteryMonitor.gui')


class battery_monitor(Gtk.Application):
	# Main initialization routine
	def __init__(self, application_id, flags):
		Gtk.Application.__init__(self, application_id=application_id, flags=flags)
		self.connect("activate", self.activate)

	def activate(self, application):
		windows = self.get_windows()
		if (len(windows) > 0):
			window = windows[0]
			window.present()
			window.show()
		else:
			window = BM_Window(self)
			self.add_window(window.window)
			window.window.show()

class BM_Window():
	"""GUI class for Settings Window.
	
	This class displays the Settings window in where the user can manage the configurations for Battery Monitor.
	"""
	
	def __init__(self, application):
		
		self.settings = Gio.Settings(schema_id="org.mamolinux.battery-monitor")
		self.icon_theme = Gtk.IconTheme.get_default()
		self.config_dir = os.path.dirname(CONFIG_FILE)
		self.config = configparser.ConfigParser()
		self.settings_updated = False
		
		# Set the Glade file
		gladefile = UI_PATH+"battery-monitor.ui"
		self.builder = Gtk.Builder()
		self.builder.add_from_file(gladefile)
		self.window = self.builder.get_object("main_window")
		self.window.set_title(_("Battery Monitor"))
		
		# Create variables to quickly access dynamic widgets
		# input values
		## Battery configuration page
		self.label_success_switch = self.builder.get_object("label_success_switch")
		self.success_switch = self.builder.get_object("success_switch")
		self.upper_threshold_warning_entry = self.builder.get_object("upper_threshold_warning")
		self.first_custom_warning_entry = self.builder.get_object("first_custom_warning")
		self.second_custom_warning_entry = self.builder.get_object("second_custom_warning")
		self.third_custom_warning_entry = self.builder.get_object("third_custom_warning")
		self.low_battery_entry = self.builder.get_object("low_battery")
		self.critical_battery_entry = self.builder.get_object("critical_battery")
		
		## Sound configuration page
		self.label_sound_switch = self.builder.get_object("label_sound_switch")
		self.sound_switch = self.builder.get_object("sound_switch")
		self.sound_filechooser_button = self.builder.get_object("sound_file")
		
		## Notification configuration page
		self.notify_duration_entry = self.builder.get_object("notify_duration")
		self.notify_count_entry = self.builder.get_object("notify_count")
		
		# Buttons
		self.save_button = self.builder.get_object("save_button")
		self.reset_button = self.builder.get_object("reset_button")
		self.quit_button = self.builder.get_object("quit_button")
		
		# Widget signals
		self.add_filters(self.sound_filechooser_button)
		self.save_button.connect('clicked', self.__save_config)
		self.reset_button.connect("clicked", self.on_reset_button)
		self.quit_button.connect('clicked', self.on_quit)
		
		# Menubar
		accel_group = Gtk.AccelGroup()
		self.window.add_accel_group(accel_group)
		menu = self.builder.get_object("main_menu")
		# Add "Shortcuts" option in drop-down menu
		item = Gtk.ImageMenuItem()
		item.set_image(Gtk.Image.new_from_icon_name("preferences-desktop-keyboard-shortcuts-symbolic", Gtk.IconSize.MENU))
		item.set_label(_("Keyboard Shortcuts"))
		item.connect("activate", self.open_keyboard_shortcuts)
		key, mod = Gtk.accelerator_parse("<Control>K")
		item.add_accelerator("activate", accel_group, key, mod, Gtk.AccelFlags.VISIBLE)
		menu.append(item)
		# Add "About" option in drop-down menu
		item = Gtk.ImageMenuItem()
		item.set_image(Gtk.Image.new_from_icon_name("help-about-symbolic", Gtk.IconSize.MENU))
		item.set_label(_("About"))
		item.connect("activate", self.__about_window, self.window)
		key, mod = Gtk.accelerator_parse("<Control>F1")
		item.add_accelerator("activate", accel_group, key, mod, Gtk.AccelFlags.VISIBLE)
		menu.append(item)
		# Add "Close" option in drop-down menu
		item = Gtk.ImageMenuItem(label=_("Close Window"))
		image = Gtk.Image.new_from_icon_name("application-exit-symbolic", Gtk.IconSize.MENU)
		item.set_image(image)
		item.connect('activate', self.on_quit)
		key, mod = Gtk.accelerator_parse("<Control>W")
		item.add_accelerator("activate", accel_group, key, mod, Gtk.AccelFlags.VISIBLE)
		menu.append(item)
		# # Add "Quit" option in drop-down menu
		# item = Gtk.ImageMenuItem(label=_("Quit"))
		# image = Gtk.Image.new_from_icon_name("application-exit-symbolic", Gtk.IconSize.MENU)
		# item.set_image(image)
		# item.connect('activate', self.__quit)
		# key, mod = Gtk.accelerator_parse("<Control>Q")
		# item.add_accelerator("activate", accel_group, key, mod, Gtk.AccelFlags.VISIBLE)
		# menu.append(item)
		# Show all drop-down menu options
		menu.show_all()
		
		self.__load_config()
		
	
	def __load_config(self):
		"""Loads configurations from config file.
		
		Tries to read and parse from config file. If the config file is missing or not readable, then it triggers default configurations.
		"""
		
		try:
			self.config.read(CONFIG_FILE)
			self.show_success = self.config['user'].getboolean('show_success')
			self.upper_threshold_warning = self.config['user']['upper_threshold_warning']
			self.first_custom_warning = self.config['user']['first_custom_warning']
			self.second_custom_warning = self.config['user']['second_custom_warning']
			self.third_custom_warning = self.config['user']['third_custom_warning']
			self.low_battery = self.config['user']['low_battery']
			self.critical_battery = self.config['user']['critical_battery']
			self.use_sound = self.config['user'].getboolean('use_sound')
			self.sound_file = self.config['user']['sound_file']
			self.notification_stability = self.config['user']['notification_stability']
			self.notification_count = self.config['user']['notification_count']
		except:
			module_logger.error('Config file is missing or not readable. Using default configurations.')
			self.show_success = True
			self.upper_threshold_warning = '90'
			self.first_custom_warning = '70'
			self.second_custom_warning = '55'
			self.third_custom_warning = '40'
			self.low_battery = '30'
			self.critical_battery = '15'
			self.use_sound = True
			self.sound_file = '/usr/share/sounds/freedesktop/stereo/dialog-warning.oga'
			self.notification_stability = '5'
			self.notification_count = '3'
		
		self.success_switch.set_active(self.show_success)
		self.upper_threshold_warning_entry.set_text(self.upper_threshold_warning)
		self.first_custom_warning_entry.set_text(self.first_custom_warning)
		self.second_custom_warning_entry.set_text(self.second_custom_warning)
		self.third_custom_warning_entry.set_text(self.third_custom_warning)
		self.low_battery_entry.set_text(self.low_battery)
		self.critical_battery_entry.set_text(self.critical_battery)
		self.sound_switch.set_active(self.use_sound)
		self.sound_filechooser_button.set_filename(self.sound_file)
		self.notify_duration_entry.set_text(self.notification_stability)
		self.notify_count_entry.set_text(self.notification_count)
		
		# Load and set new labels of switches based on saved configuration
		if self.show_success:
			self.label_success_switch.set_label("Disable Success Notification:")
		else:
			self.label_success_switch.set_label("Enable Success Notification:")
		
		if self.use_sound:
			self.label_sound_switch.set_label("Disable Notification Sound:")
		else:
			self.label_sound_switch.set_label("Enable Notification Sound:")
	
	def __save_config(self, widget):
		"""Saves configurations to config file.

		Saves user-defined configurations to config file. If
		the config file does not exist, it creates a new config
		file (~/.config/battery-monitor/battery-monitor.cfg) in
		user's home directory.
		"""
		
		if os.path.exists(self.config_dir):
			pass
		else:
			os.makedirs(self.config_dir)
		
		self.config['user'] = {
			'show_success': self.success_switch.get_active(),
			'upper_threshold_warning': self.upper_threshold_warning_entry.get_text(),
			'first_custom_warning': self.first_custom_warning_entry.get_text(),
			'second_custom_warning': self.second_custom_warning_entry.get_text(),
			'third_custom_warning': self.third_custom_warning_entry.get_text(),
			'low_battery': self.low_battery_entry.get_text(),
			'critical_battery': self.critical_battery_entry.get_text(),
			'use_sound': self.sound_switch.get_active(),
			'sound_file': self.sound_filechooser_button.get_filename(),
			'notification_stability': self.notify_duration_entry.get_text(),
			'notification_count': self.notify_count_entry.get_text()
		}
		
		try:
			self.__validate_config(self.config['user'])
			with open(CONFIG_FILE, 'w') as f:
				self.config.write(f)
				dialog = Gtk.MessageDialog(message_type=Gtk.MessageType.INFO)
				dialog.set_transient_for(self.window)
				dialog.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)
				dialog.set_property("text", _('Successfully Saved!'))
				dialog.format_secondary_text(_('Your settings have been saved successfully.'))
				response = dialog.run()
				if response == Gtk.ResponseType.OK:
					self.save_button.set_sensitive(False)
				dialog.destroy()
		except ValidationError as message:
			dialog = Gtk.MessageDialog(message_type=Gtk.MessageType.ERROR)
			dialog.set_transient_for(self.window)
			dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ButtonsType.CANCEL)
			dialog.set_property("text", _('Validation Error!'))
			dialog.format_secondary_text(str(message))
			dialog.run()
			dialog.destroy()
		
		self.settings_updated = True
		self.__load_config()
	
	def __validate_config(self, config):
		"""validates config before saving to config file."""
		
		if bool(config['upper_threshold_warning']):
			if int(config['upper_threshold_warning']) <= 0:
				raise ValidationError(_('Upper threshold Warning must be greater than zero.'))
		
		if bool(config['second_custom_warning']) and bool(config['first_custom_warning']):
			if int(config['second_custom_warning']) >= int(config['first_custom_warning']):
				raise ValidationError(_('The value of first custom warning must be greater than then value of second custom warning.'))
		
		if bool(config['third_custom_warning']) and bool(config['second_custom_warning']):
			if int(config['third_custom_warning']) >= int(config['second_custom_warning']):
				raise ValidationError(_('The value of second custom warning must be greater than the value 0f third custom warning.'))
		
		if bool(config['low_battery']) and bool(config['third_custom_warning']):
			if int(config['low_battery']) >= int(config['third_custom_warning']):
				raise ValidationError(_('The value of third custom warning must be greater than the value of low battery warning.'))
		
		if bool(config['critical_battery']) and bool(config['low_battery']):
			if int(config['critical_battery']) >= int(config['low_battery']):
				raise ValidationError(_('The value of low battery warning must be greater than the value of critical battery warning.'))
		else:
			if bool(config['critical_battery']):
				raise ValidationError(_('Low battery warning can not be empty.'))
			else:
				raise ValidationError(_('Critical battery warning can not be empty.'))
		
		if bool(config['notification_stability']):
			if int(config['notification_stability']) <= 0:
				raise ValidationError(_('Notification stability time must be greater than zero.'))
		else:
			raise ValidationError(_('Notification stability time can not be empty.'))
		
		if bool(config['notification_count']):
			if int(config['notification_count']) <= 0:
				raise ValidationError(_('Notification count must be greater than zero.'))
		else:
			raise ValidationError(_('Notification count can not be empty.'))
	
	def on_reset_button(self, widget):
		'''
		Reset to defaut settings.
		'''
		dialog = Gtk.MessageDialog(message_type=Gtk.MessageType.WARNING)
		dialog.set_transient_for(self.window)
		dialog.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK, Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
		dialog.set_property("text", _('Restore default settings?'))
		dialog.format_secondary_text(_('Click ok to restore and save default settings successfully.'))
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			try:
				# Try reading the config file for defaut settings.
				self.config.read(CONFIG_FILE)
				
				self.show_success = self.config['default'].getboolean('show_success')
				self.upper_threshold_warning = int(self.config['default']['upper_threshold_warning'])
				self.first_custom_warning = int(self.config['default']['first_custom_warning'])
				self.second_custom_warning = int(self.config['default']['second_custom_warning'])
				self.third_custom_warning = int(self.config['default']['third_custom_warning'])
				self.low_battery = int(self.config['default']['low_battery'])
				self.critical_battery = int(self.config['default']['critical_battery'])
				
				self.use_sound = self.config['default'].getboolean('use_sound')
				self.sound_file = self.config['default']['sound_file']
				
				self.notification_stability = int(self.config['default']['notification_stability'])
				self.notification_count = int(self.config['default']['notification_count'])
			except:
				# In case defaut settings is corrupted in config file
				# set them again
				module_logger.error('Default configuration in config file is corrupted. Again setting the default values.')
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
			
			# Reload the GUI with default settings.
			self.success_switch.set_active(self.show_success)
			self.upper_threshold_warning_entry.set_text(str(self.upper_threshold_warning))
			self.first_custom_warning_entry.set_text(str(self.first_custom_warning))
			self.second_custom_warning_entry.set_text(str(self.second_custom_warning))
			self.third_custom_warning_entry.set_text(str(self.third_custom_warning))
			self.low_battery_entry.set_text(str(self.low_battery))
			self.critical_battery_entry.set_text(str(self.critical_battery))
			self.sound_switch.set_active(self.use_sound)
			self.sound_filechooser_button.set_filename(self.sound_file)
			self.notify_duration_entry.set_text(str(self.notification_stability))
			self.notify_count_entry.set_text(str(self.notification_count))
			
			# Save the default settings as 'user' settings
			self.config['user'] = {
				'show_success': self.success_switch.get_active(),
				'upper_threshold_warning': self.upper_threshold_warning_entry.get_text(),
				'first_custom_warning': self.first_custom_warning_entry.get_text(),
				'second_custom_warning': self.second_custom_warning_entry.get_text(),
				'third_custom_warning': self.third_custom_warning_entry.get_text(),
				'low_battery': self.low_battery_entry.get_text(),
				'critical_battery': self.critical_battery_entry.get_text(),
				'use_sound': self.sound_switch.get_active(),
				'sound_file': self.sound_filechooser_button.get_filename(),
				'notification_stability': self.notify_duration_entry.get_text(),
				'notification_count': self.notify_count_entry.get_text()
			}
			with open(CONFIG_FILE, 'w') as f:
				self.config.write(f)
			# module_logger.info()
		else:
			pass
		dialog.destroy()
	
	def __about_window(self, signal, widget):
		about_window = AboutWindow(widget)
		about_window.show()
	
	def open_keyboard_shortcuts(self, widget):
		gladefile = UI_PATH+"shortcuts.ui"
		builder = Gtk.Builder()
		builder.set_translation_domain(APP)
		builder.add_from_file(gladefile)
		window = builder.get_object("shortcuts-batterymonitor")
		window.set_title(_("Battery Monitor"))
		window.show()
	
	def on_quit(self, widget):
		self.window.close()
	
	def add_filters(self, dialog):
		'''
		Filter audio files to be used for notification sound
		'''
		filter_audio = Gtk.FileFilter()
		filter_audio.set_name("Audio files")
		filter_audio.add_mime_type("audio/*")
		dialog.add_filter(filter_audio)

		filter_any = Gtk.FileFilter()
		filter_any.set_name("Any files")
		filter_any.add_pattern("*")
		dialog.add_filter(filter_any)


def run_BMwindow():
	application = battery_monitor("org.mamolinux.battery-monitor", Gio.ApplicationFlags.FLAGS_NONE)
	application.run()
