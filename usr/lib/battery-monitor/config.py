#!/usr/bin/env python3

# standard library
import gettext
import locale
import os


# i18n
APP = 'battery-monitor'
LOCALE_DIR = "/usr/share/locale"
locale.bindtextdomain(APP, LOCALE_DIR)
gettext.bindtextdomain(APP, LOCALE_DIR)
gettext.textdomain(APP)
_ = gettext.gettext

_path = os.path.dirname(os.path.abspath(__file__))
_icon_path = _path + '/icons/'

APPINDICATOR_ID = 'battery-monitor'

CONFIG_FILE = os.path.expanduser('~/.config/battery-monitor/battery-monitor.cfg')

ICONS = {
    "app": "tray-icon.svg",
    "success": "icon.png",
    "fail": "icon.png",
    "acpi": "icon.png",
    "charging": "charging.png",
    "discharging": "discharging.png",
    "full":  "full-charge.png",
    "unknown":  "not-charging.png",
    "low_battery": "low-battery.png",
    "critical_battery": "critical-battery.png",
    "first_custom_warning": "discharging.png",
    "second_custom_warning": "discharging.png",
    "third_custom_warning": "discharging.png",
    "upper_threshold_warning": "charging.png"
}

for key in ICONS:
	ICONS[key] = _icon_path + ICONS[key]

MESSAGES = {
    "success": (
        _("Battery Monitor"),
        _("Cheers! Your battery is being monitored now.")
    ),

    "fail": (
        _("Battery Monitor"),
        _("Alas! Battery is not yet present!")
    ),

    "acpi": (
        _("Battery Monitor"),
        _("Dependency Error! acpi is not installed.")
    ),

    "charging": (
        _("Charging"),
        _("Now {battery_percentage} %, {remaining_time}")
    ),

    "discharging": (
        _("Discharging"),
        _("Now {battery_percentage} %, {remaining_time}")
    ),

    "full": (
        _("Fully Charged - Unplug your Charger"),
        _("{battery_percentage} % Remaining")
    ),

    "unknown": (
        _("Fully Charged"),
        _("{battery_percentage} % Remaining")
    ),

    "low_battery": (
        _("Low Battery"),
        _("Now {battery_percentage} %, {remaining_time}")
    ),

    "critical_battery": (
        _("Critically Low Battery"),
        _("Only {battery_percentage} %, {remaining_time}")
    ),

    "first_custom_warning": (
        _("First Custom Warning"),
        _("Now {battery_percentage} %, {remaining_time}")
    ),

    "second_custom_warning": (
        _("Second Custom Warning"),
        _("Now {battery_percentage} %, {remaining_time}")
    ),

    "third_custom_warning": (
        _("Third Custom Warning"),
        _("Now {battery_percentage} %, {remaining_time}")
    ),
    "upper_threshold_warning": (
        _("Upper Threshold Warning - Unplug your Charger"),
        _("Now {battery_percentage} %, {remaining_time}")
    )
}

TEST_CASES = {
    "state": [
        _("Full"),
        _("Charging"),
        _("Discharging")
    ],
    "remaining": [
        _("00:10:12 remaining"),
        _("01:47:31 remaining"),
        _("02:33:47 remaining"),
        _("03:24:25 remaining"),
        _("discharging at zero rate - will never fully discharge")
    ]
}
