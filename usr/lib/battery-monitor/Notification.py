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


class Notification:
    """Triggers notification on battery state changes.

    Triggers informative and effective notification on every change of battery state.
    """
    
    if platform.python_version() >= '3.6':
        TEST_MODE: bool
        last_notification: str
        last_percentage: int

    def __init__(self, type: str, TEST_MODE: bool = False) -> None:
        
        self.monitor = BatteryMonitor(TEST_MODE)
        self.config = configparser.ConfigParser()
        self.load_config()
        
        # initiating notification
        Notify.init(_("Battery Monitor"))
        message = MESSAGES[type]
        head = message[0]
        body = message[1]
        icon = ICONS[type]
        self.last_percentage = 0
        self.last_notification = ''
        self.notifier = Notify.Notification()
        self.notification = self.notifier.new(head, body, icon)
        self.notification.set_urgency(Notify.Urgency.CRITICAL)
        # TODO: This is like fighting against ourselves. Make better fix.
        # silence 'success' notification
        if (type != "success"):
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
                self.critical_battery = int(self.config['settings']['critical_battery'])
            except ValueError:
                self.critical_battery = 10
            try:
                self.low_battery = int(self.config['settings']['low_battery'])
            except ValueError:
                self.low_battery = 30
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
                self.notification_stability = int(self.config['settings']['notification_stability'])
            except ValueError:
                self.notification_stability = 5
            try:
                self.upper_threshold_warning = int(self.config['settings']['upper_threshold_warning'])
            except ValueError:
                self.upper_threshold_warning = 90
        except:
            print('Config file is missing or not readable. Using default configurations.')
            self.critical_battery = 10
            self.low_battery = 30
            self.first_custom_warning = -1
            self.second_custom_warning = -2
            self.third_custom_warning = -3
            self.notification_stability = 5
            self.upper_threshold_warning = 90

    def show_notification(self, type: str, battery_percentage: int,
                          remaining_time: str = None, _count: int = 5) -> None:
        
        message = MESSAGES[type]
        head = message[0]
        body = message[1].format(battery_percentage=battery_percentage,
                                 remaining_time=remaining_time)
        icon = ICONS[type]
        # self.notifier.update(head, body, icon)
        # notification = self.notifier.new(head, body, icon)
        try:
            for i in range(_count):
                if self.monitor.is_updated():
                    continue
                # self.notifier.show()
                notification = self.notifier.new(head, body, icon)
                notification.show()
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

        if state == 'discharging':
            if (percentage != self.last_percentage and
                remaining != "discharging at zero rate - will never fully discharge"):
                self.last_percentage = percentage
                if percentage <= self.critical_battery:
                    self.last_notification = "critical_battery"
                    self.show_notification(type="critical_battery",
                                           battery_percentage=percentage,
                                           remaining_time=remaining)

                    return "critical_battery"

                elif (percentage <= self.low_battery and
                      self.last_notification != "low_battery"):
                    self.last_notification = "low_battery"
                    self.show_notification(type="low_battery",
                                           battery_percentage=percentage,
                                           remaining_time=remaining)

                    return "low_battery"

                elif (percentage <= self.third_custom_warning and
                      self.last_notification != "third_custom_warning"):
                    self.last_notification = "third_custom_warning"
                    self.show_notification(type="third_custom_warning",
                                           battery_percentage=percentage,
                                           remaining_time=remaining)

                    return "third_custom_warning"

                elif (percentage <= self.second_custom_warning and
                      self.last_notification != "second_custom_warning"):
                    self.last_notification = "second_custom_warning"
                    self.show_notification(type="second_custom_warning",
                                           battery_percentage=percentage,
                                           remaining_time=remaining)

                    return "second_custom_warning"

                elif (percentage <= self.first_custom_warning and
                      self.last_notification != "first_custom_warning"):
                    self.last_notification = "first_custom_warning"
                    self.show_notification(type="first_custom_warning",
                                           battery_percentage=percentage,
                                           remaining_time=remaining)

                    return "first_custom_warning"

        elif state == 'charging':
            if (percentage != self.last_percentage and
                remaining != "discharging at zero rate - will never fully discharge" and
                self.last_notification!="upper_threshold_warning" and
                percentage >= self.upper_threshold_warning):
                    self.last_percentage = percentage
                    self.last_notification!="upper_threshold_warning"
                    self.show_notification(type="upper_threshold_warning",
                                           battery_percentage=percentage,
                                           remaining_time=remaining)

                    return "upper_threshold_warning"
        
        else:
            """
                if last notification = charging, so is charging now than, the preceding block will not work.
            """
            if state != self.last_notification and remaining != "discharging at zero rate - will never fully discharge":
                self.last_notification = state
                self.show_notification(type=state,
                                       battery_percentage=percentage,
                                       remaining_time=remaining)

                return state

    def __del__(self):
        self.notifier.close()
        Notify.uninit()
