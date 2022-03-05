#!/usr/bin/env python3

# standard library
import gettext
import locale
import platform
import random
import subprocess
from typing import Dict

# imports from current project
from config import TEST_CASES


# i18n
APP = 'battery-monitor'
LOCALE_DIR = "/usr/share/locale"
locale.bindtextdomain(APP, LOCALE_DIR)
gettext.bindtextdomain(APP, LOCALE_DIR)
gettext.textdomain(APP)
_ = gettext.gettext

class BatteryMonitor:
    if platform.python_version() >= '3.6':
        raw_battery_info: str
        processed_battery_info: Dict[str, str]
    
    def __init__(self, TEST_MODE):
        self.TEST_MODE = TEST_MODE
        self.raw_battery_info = self.get_raw_battery_info()
        self.processed_battery_info = self.get_processed_battery_info()
    
    def get_raw_battery_info(self):
        if self.TEST_MODE:
            state = random.choice(TEST_CASES['state'])
            percentage = str(random.randint(0, 100))
            remaining = random.choice(TEST_CASES['remaining'])
            result = "Battery 0: " + state + ", " + percentage + "%, " + remaining
            print(result)
            return result.encode('UTF-8')
        else:
            command = "acpi -b"
            raw_info = subprocess.check_output(command,
                                            stderr=subprocess.PIPE,
                                            shell=True)
            print(raw_info)
        return raw_info
    
    def is_updated(self):
        current_raw_info = self.get_raw_battery_info()
        if self.raw_battery_info != current_raw_info:
            self.raw_battery_info = current_raw_info
            print("True")
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
