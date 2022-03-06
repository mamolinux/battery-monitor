#!/usr/bin/env python3

# standard library
import configparser
import gettext
import locale
import os

# third-party library
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

# imports from current project
from config import CONFIG_FILE
from AboutWindow import AboutWindow
from ErrorLib import ValidationError
# from AppIndicator import bm_daemon

# i18n
APP = 'battery-monitor'
LOCALE_DIR = "/usr/share/locale"
locale.bindtextdomain(APP, LOCALE_DIR)
gettext.bindtextdomain(APP, LOCALE_DIR)
gettext.textdomain(APP)
_ = gettext.gettext


class bm_settings(Gtk.Application):
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
			window = SettingsWindow(self)
			self.add_window(window.window)
			window.window.show()

class SettingsWindow():
	"""GUI class for Settings Window.
	
	This class displays the Settings window in where the user can manage the configurations for Battery Monitor.
	"""
	
	def __init__(self, application):
		
		self.settings = Gio.Settings(schema_id="org.x.battery-monitor")
		self.icon_theme = Gtk.IconTheme.get_default()
		# self.set_default_icon_from_file(ICONS['app'])
		self.config_dir = os.path.dirname(CONFIG_FILE)
		self.config = configparser.ConfigParser()
		self.settings_updated = False
		
		# Set the Glade file
		gladefile = "/usr/share/battery-monitor/battery-monitor.ui"
		self.builder = Gtk.Builder()
		self.builder.add_from_file(gladefile)
		self.window = self.builder.get_object("main_window")
		self.window.set_title(_("Battery Monitor"))
		
		# Create variables to quickly access dynamic widgets
		# input values
		## Battery configuration page
		self.success_shown_entry = self.builder.get_object("success_shown")
		self.upper_threshold_warning_entry = self.builder.get_object("upper_threshold_warning")
		self.first_custom_warning_entry = self.builder.get_object("first_custom_warning")
		self.second_custom_warning_entry = self.builder.get_object("second_custom_warning")
		self.third_custom_warning_entry = self.builder.get_object("third_custom_warning")
		self.low_battery_entry = self.builder.get_object("low_battery")
		self.critical_battery_entry = self.builder.get_object("critical_battery")
		
		## Sound configuration page
		self.label_sound_switch = self.builder.get_object("label_sound_switch")
		self.sound_switch = self.builder.get_object("sound_switch")
		self.sound_file_entry = self.builder.get_object("sound_file")
		
		## Notification configuration page
		self.notify_duration_entry = self.builder.get_object("notify_duration")
		self.notify_count_entry = self.builder.get_object("notify_count")
		
		# Buttons
		self.save_button = self.builder.get_object("save_button")
		self.quit_button = self.builder.get_object("quit_button")
		
		# Widget signals
		self.save_button.connect('clicked', self.__save_config)
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
		item.connect("activate", self.__about_window)
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
			self.success_shown = self.config['settings']['success_shown']
			self.upper_threshold_warning = self.config['settings']['upper_threshold_warning']
			self.first_custom_warning = self.config['settings']['first_custom_warning']
			self.second_custom_warning = self.config['settings']['second_custom_warning']
			self.third_custom_warning = self.config['settings']['third_custom_warning']
			self.low_battery = self.config['settings']['low_battery']
			self.critical_battery = self.config['settings']['critical_battery']
			self.use_sound = int(self.config['settings']['use_sound'])
			self.notification_stability = self.config['settings']['notification_stability']
			self.notification_count = self.config['settings']['notification_count']
		except:
			print('Config file is missing or not readable. Using default configurations.')
			self.success_shown = "No"
			self.upper_threshold_warning = '90'
			self.first_custom_warning = '70'
			self.second_custom_warning = '55'
			self.third_custom_warning = '40'
			self.low_battery = '30'
			self.critical_battery = '15'
			self.use_sound = 1
			self.notification_stability = '5'
			self.notification_count = '5'
		
		self.success_shown_entry.set_text(self.success_shown)
		self.upper_threshold_warning_entry.set_text(self.upper_threshold_warning)
		self.first_custom_warning_entry.set_text(self.first_custom_warning)
		self.second_custom_warning_entry.set_text(self.second_custom_warning)
		self.third_custom_warning_entry.set_text(self.third_custom_warning)
		self.low_battery_entry.set_text(self.low_battery)
		self.critical_battery_entry.set_text(self.critical_battery)
		self.sound_switch.set_active(self.use_sound)
		self.notify_duration_entry.set_text(self.notification_stability)
		self.notify_count_entry.set_text(self.notification_count)
	
	def __save_config(self, widget):
		"""Saves configurations to config file.

		Saves user-defined configurations to config file. If the config file does not exist, it creates a new config file (~/.config/battery-monitor/battery-monitor.cfg) in user's home directory.
		"""
		
		if os.path.exists(self.config_dir):
			pass
		else:
			os.makedirs(self.config_dir)
		
		if self.sound_switch.get_active():
			use_sound = 1
		else:
			use_sound = 0
		
		self.config['settings'] = {
			'success_shown': self.success_shown_entry.get_text(),
			'upper_threshold_warning': self.upper_threshold_warning_entry.get_text(),
			'first_custom_warning': self.first_custom_warning_entry.get_text(),
			'second_custom_warning': self.second_custom_warning_entry.get_text(),
			'third_custom_warning': self.third_custom_warning_entry.get_text(),
			'low_battery': self.low_battery_entry.get_text(),
			'critical_battery': self.critical_battery_entry.get_text(),
			'use_sound': use_sound,
			'notification_stability': self.notify_duration_entry.get_text(),
			'notification_count': self.notify_count_entry.get_text()
		}
		
		try:
			self.__validate_config(self.config['settings'])
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
	
	def __about_window(self, *args):
		about_window = AboutWindow()
		about_window.show()
	
	def open_keyboard_shortcuts(self, widget):
		gladefile = "/usr/share/battery-monitor/shortcuts.ui"
		builder = Gtk.Builder()
		builder.set_translation_domain(APP)
		builder.add_from_file(gladefile)
		window = builder.get_object("shortcuts-batterymonitor")
		window.set_title(_("Battery Monitor"))
		window.show()

	def on_quit(self, widget):
		self.window.close()
	
	# def __quit(self, *args):
	# 	Gtk.main_quit()
		