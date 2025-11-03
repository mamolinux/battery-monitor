# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#  Battery Monitor – Maximize Your Battery Life.
#  Copyright (C) 2016–2020 Maksudur Rahman Maateen
#  Copyright (C) 2021–2025 Himadri Sekhar Basu
#  Licensed under GPLv3 or later (see <http://www.gnu.org/licenses/>)
# -----------------------------------------------------------------------------

# standard library
import gettext
import locale

# third-party library
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# imports from current project
from BatteryMonitor.cli_args import APP, LOCALE_DIR, description
from BatteryMonitor.config import __version__

# i18n
locale.bindtextdomain(APP, LOCALE_DIR)
gettext.bindtextdomain(APP, LOCALE_DIR)
gettext.textdomain(APP)
_ = gettext.gettext


class AboutWindow():
	"""GUI class for About Window.

	This class displays the About window in where the user can see the information about Battery Monitor project.
	"""

	def __init__(self, widget):
		authors = [
			'Himadri Sekhar Basu <https://hsbasu.github.io>',
			'Maksudur Rahman Maateen <https://maateen.me/>',
			'Safwan Rahman <https://github.com/safwanrahman>',
			'Abdelhak BOUGOUFFA <https://abougouffa.github.io/>'
		]
		copyrights = "Copyright \xa9 2016-2018 Maksudur Rahman Maateen\n \
			Copyright \xa9 2021-2024 Himadri Sekhar Basu"
		documenters = [
			'Maksudur Rahman Maateen <https://maateen.me/>'
		]
		mainatainers = [
			'Himadri Sekhar Basu <https://hsbasu.github.io>'
		]

		# initiaing about dialog and params
		self.about_dialog = Gtk.AboutDialog()
		self.about_dialog.set_transient_for(widget)
		
		self.about_dialog.set_icon_name("battery-monitor")
		self.about_dialog.set_title(_("About"))
		
		self.about_dialog.set_logo_icon_name("battery-monitor")
		self.about_dialog.set_program_name(_('Battery Monitor'))
		self.about_dialog.set_version(__version__)
		
		self.about_dialog.set_website_label('Official Website')
		self.about_dialog.set_website('https://hsbasu.github.io/battery-monitor/')
		self.about_dialog.set_comments(description)
		self.about_dialog.set_copyright(copyrights)
		
		self.about_dialog.set_authors(authors)
		self.about_dialog.set_documenters(documenters)
		# self.about_dialog.add_credit_section('AUR maintained by', ['Yochanan Marqos <https://github.com/yochananmarqos>'])
		self.about_dialog.add_credit_section(_('Maintainer'), mainatainers)
		
		try:
			h = open('/usr/share/common-licenses/GPL', encoding="utf-8")
			s = h.readlines()
			gpl = ""
			for line in s:
				gpl += line
			h.close()
			self.about_dialog.set_license(gpl)
		except Exception as e:
			print(e)
		
		self.about_dialog.connect('response', self.__close)

	def show(self):
		# show the about dialog.
		self.about_dialog.show()

	def __close(self, action, parameter):
		"""Called when the user wants to close the about dialog.

		@param: action
			the window to close
		"""
		action.destroy()
