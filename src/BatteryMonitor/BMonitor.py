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
import platform
import random
import subprocess
from typing import Dict

# imports from current project
from BatteryMonitor.cli_args import APP, LOCALE_DIR
from BatteryMonitor.config import TEST_CASES


# i18n
locale.bindtextdomain(APP, LOCALE_DIR)
gettext.bindtextdomain(APP, LOCALE_DIR)
gettext.textdomain(APP)
_ = gettext.gettext

# log
module_logger = logging.getLogger('BatteryMonitor.BMonitor')


# This is the backend.
# It contains utility functions to
# monitor battery states
class BMonitor:
    if platform.python_version() >= '3.6':
        raw_battery_info: str
        processed_battery_info: Dict[str, str]
    
    def __init__(self, TEST_MODE):
        module_logger.debug("Initiating Battery Monitor")
        self.TEST_MODE = TEST_MODE
        self.raw_battery_info = self.get_raw_battery_info()
        self.processed_battery_info = self.get_processed_battery_info()
    
    def get_raw_battery_info(self):
        if self.TEST_MODE:
            state = random.choice(TEST_CASES['state'])
            percentage = str(random.randint(0, 100))
            remaining = random.choice(TEST_CASES['remaining'])
            result = "Battery 0: " + state + ", " + percentage + "%, " + remaining
            module_logger.debug(result)
            return result.encode('UTF-8')
        else:
            command = "acpi -b"
            raw_info = subprocess.check_output(command,
                                            stderr=subprocess.PIPE,
                                            shell=True)
            module_logger.debug(raw_info.decode("utf-8", "strict").strip('\n'))
        return raw_info
    
    def is_updated(self):
        current_raw_info = self.get_raw_battery_info()
        if self.raw_battery_info != current_raw_info:
            self.raw_battery_info = current_raw_info
            module_logger.debug("Battery state updated")
            return True
        
        return False
    
    def get_processed_battery_info(self):
        processed_battery_info = {}
        in_list = (self.raw_battery_info.decode("utf-8", "strict").lower().strip('\n')
                    .split(": ", 1)[1].split(", "))
        try:
            processed_battery_info["state"] = in_list[0]
            processed_battery_info["percentage"] = in_list[1]
            processed_battery_info["remaining"] = in_list[2]
        except IndexError:
            pass
        
        return processed_battery_info
