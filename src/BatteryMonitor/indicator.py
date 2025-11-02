# Copyright: 2016-2020 Maksudur Rahman Maateen <maateen@outlook.com>
#            2021-2024 Himadri Sekhar Basu <hsb10@iitbbs.ac.in>
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
import os         # Added for PID and file operations
import fcntl      # Added for file locking
import sys        # Added for exiting and process management
import signal     # Added for sending termination signals
import time       # Added for brief sleep while waiting for old process to die
import errno      # Added for specific IOError checking
import atexit # Moved from inside a function to the top

# third-party library
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

try:
    gi.require_version('AyatanaAppIndicator3', '0.1')
    from gi.repository import AyatanaAppIndicator3 as appindicator
except (ValueError, ImportError):
    try:
        gi.require_version('AppIndicator3', '0.1')
        from gi.repository import AppIndicator3 as appindicator
    except (ValueError, ImportError):
        print("Required indicator library not found.")
        appindicator = None

# imports from current project
from BatteryMonitor.cli_args import APP, LOCALE_DIR
from BatteryMonitor.about_window import AboutWindow
from BatteryMonitor.bm_daemon import BMdaemon
from BatteryMonitor.gui import run_BMwindow
from BatteryMonitor.config import LOGPATH


# i18n
locale.bindtextdomain(APP, LOCALE_DIR)
gettext.bindtextdomain(APP, LOCALE_DIR)
gettext.textdomain(APP)
_ = gettext.gettext

# log
module_logger = logging.getLogger('BatteryMonitor.indicator')

# Define PID file path globally
PID_FILE = os.path.join(LOGPATH, f".{APP}.pid")

class BMIndicator():
	"""Class for system tray icon.
	
	This class will show Battery Monitor icon in system tray.
	"""
	def __init__(self, TEST_MODE: bool = False):
		self.lock_file_handle = None
		
		# Check for existing instance and kill it if necessary
		if not self.acquire_lock_or_kill_previous():
			# If acquisition failed even after trying to kill, something is wrong
			module_logger.error(_("Could not acquire lock or kill previous instance."))
			sys.exit(1)
		
		module_logger.debug(_("Initiaing Appindicator."))
		self.indicator = appindicator.Indicator.new(APP, APP, appindicator.IndicatorCategory.SYSTEM_SERVICES)
		self.indicator.set_title(_('Battery Monitor'))
		self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
		
		# run the daemon
		self.daemon = BMdaemon(TEST_MODE)
		
		# create menu
		self.indicator.set_menu(self.__create_menu())
		
		# Override Gtk.main_quit to ensure cleanup happens on exit
		self._original_gtk_quit = Gtk.main_quit
		Gtk.main_quit = self.__quit # Use our own quit handler for cleanup
		
		Gtk.main()
	
	def acquire_lock_or_kill_previous(self):
		"""
		Attempts to acquire an exclusive lock. Kills previous if necessary.
		"""
		
		old_pid = None
		try:
			with open(PID_FILE, 'r') as f:
				old_pid_str = f.read().strip()
				if old_pid_str:
					old_pid = int(old_pid_str)
		except (IOError, ValueError):
			# File doesn't exist or is corrupted/empty
			old_pid = None
		
		# Try to acquire lock immediately
		try:
			self.generate_lock()
			return True # Successfully acquired lock
		
		except IOError as e:
			if e.errno != errno.EWOULDBLOCK:
				# Some other serious IO error
				raise
			
			# Lock acquisition failed (another instance is running)
			if old_pid:
				module_logger.info(_(f"Existing instance found with PID {old_pid}. Attempting to terminate it."))
				try:
					# Send a signal to terminate the old process gracefully (SIGTERM)
					os.kill(old_pid, signal.SIGTERM)
					
					# Wait briefly for the old process to exit gracefully
					time.sleep(2) 
					
					# Now we restart the current script process using os.execv, ensuring it re-runs this logic fresh.
					module_logger.info(_("Old instance termination requested. Rerunning new instance via os.execv to take over."))
					
					# Note: os.execv replaces the current process entirely, so we don't return here.
					os.execv(sys.executable, [sys.executable] + sys.argv)
					
				except OSError as e_kill:
					module_logger.error(_(f"Could not kill previous instance (PID {old_pid}): {e_kill}"))
					return False # Exit if unable to take over
			else:
				module_logger.error(_("Lock exists but no valid PID found in file. Manual cleanup required."))
				return False


	def generate_lock(self):
		"""
		Generates a new lock file and registers cleanup.
		"""
		pid = os.getpid()
		self.lock_file_handle = open(PID_FILE, 'w')
		# Write the current PID to the lock file
		self.lock_file_handle.write(str(pid))
		self.lock_file_handle.flush()
		
		# Try to acquire a lock immediately (LOCK_NB). Raises IOError if locked.
		fcntl.flock(self.lock_file_handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
		
		# If successful, register an atexit function to release the lock
		atexit.register(self.cleanup_pid_file)
		module_logger.info(_(f"Lock acquired (PID: {pid}). Running as primary instance."))
	
	def cleanup_pid_file(self, *args):
		"""Releases the lock and removes the PID file."""
		module_logger.debug(_("Releasing lock and removing the PID file."))
		
		# Check if the handle is valid and still open
		if self.lock_file_handle and not self.lock_file_handle.closed:
			try:
				# 1. Release the lock
				fcntl.flock(self.lock_file_handle, fcntl.LOCK_UN)
			except Exception as e:
				# This might happen if the file was deleted externally right before this
				module_logger.warning(_(f"Error during lock release: {e}"))
			
			try:
				# 2. Close the file handle
				self.lock_file_handle.close()
			except Exception as e:
				module_logger.warning(_(f"Error during file close: {e}"))
			
			# 3. Set the handle to None so subsequent calls do nothing
			self.lock_file_handle = None
		
		# 4. Ensure the file on disk is removed, handling potential race conditions
		if os.path.exists(PID_FILE):
			try:
				os.remove(PID_FILE)
				module_logger.debug(_(f"Removed PID file: {PID_FILE}"))
			except OSError as e:
				module_logger.warning(_(f"Error removing PID file {PID_FILE}: {e}"))

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
		# Our custom quit handler that ensures lock cleanup occurs
		self.cleanup_pid_file()
		self._original_gtk_quit() # Call the original Gtk function
