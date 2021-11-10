# [Battery Monitor]( https://hsbasu.github.io/battery-monitor)

Battery Monitor is a utility tool developed on Python3 and PyGtk3. It will notify the user about charging, discharging, not charging and critically low battery state of the battery on Linux (surely if the battery is present).

 - [Dependencies](#dependencies)
 - [Installation](#installation)
     - [Common Method](#common-method)
     - [For Ubuntu and its derivatives](#for-ubuntu-and-its-derivatives)
     - [For Arch Linux and its derivatives](#for-arch-linux-and-its-derivatives)
     - [For Beta Testers](#for-beta-testers)
     - [For Developers](#for-developers)
 - [Uninstall Daily Build](#uninstall-daily-build)
 - [User Manual](#user-manual)
     - [Auto Start](#auto-start)
     - [Settings](#settings)
 - [Issue Tracking](#issue-tracking)
 - [Screenshots](#screenshots)
     - [Initial State](#initial-state)
     - [Charging State](#charging-state)
     - [Discharging State](#discharging-state)
     - [Not Charging State](#not-charging-state)
     - [Critically Low Battery State](#critically-low-battery-state)
 - [Roadmap](#roadmap)
 - [Changelog](#changelog)
 - [Contributors](#contributors)
 
## Uninstall Daily Build

```shell
$ sudo systemctl stop battery-monitor
$ sudo systemctl disable battery-monitor
$ sudo rm -f /usr/local/bin/battery-monitor
$ sudo rm -rf /etc/battery-monitor
$ sudo rm -f /etc/systemd/system/battery-monitor.service
$ sudo systemctl daemon-reload
```

## Dependencies

* acpi
* python3
* python3-gi
* python3-setuptools
* libnotify4
* libappindicator3-1
* gir1.2-appindicator3-0.1

To use **Battery Monitor** you need these dependencies installed on your PC.

## Installation

### Common Method

```
wget https://github.com/maateen/battery-monitor/archive/master.zip
unzip master.zip
cd battery-monitor-master
sudo make install
```
That's all. **Battery Monitor (Stable)** is installed on your system.

### For Ubuntu and its derivatives (Not Working)

Let's install from PPA (currently supported: **14.04**, **17.10** & **18.04**; we're struggling with Ubuntu 16.04 right now):

```
sudo add-apt-repository ppa:maateen/battery-monitor -y
sudo apt-get update
sudo apt-get install battery-monitor -y
```
That's all. **Battery Monitor (Stable)** is installed on your system.

### For Arch Linux and its derivatives

The stable version, git version and the beta version are available in the [Arch User Repository](https://aur.archlinux.org/):

Stable: [`battery-monitor`](https://aur.archlinux.org/packages/battery-monitor)
Git: [`battery-monitor-git`](https://aur.archlinux.org/packages/battery-monitor-git)
Beta: [`battery-monitor-devel-git`](https://aur.archlinux.org/packages/battery-monitor-devel-git)

If you're not sure how to use the AUR, please see the [Manjaro](https://wiki.manjaro.org/index.php/Arch_User_Repository) and [Arch](https://wiki.archlinux.org/index.php/Arch_User_Repository#What_is_the_AUR.3F) wiki entries about it. You will need an [AUR helper](https://wiki.archlinux.org/index.php/AUR_helpers) to install packages.

### For Beta Testers

```
wget https://github.com/hsbasu/battery-monitor/archive/devel.zip
unzip devel.zip
cd battery-monitor-devel
sudo make install
```
That's all. **Battery Monitor (Beta)** is installed on your system.

### For Developers
Now you can automatically test **Battery Monitor** from Terminal:

```
python3 run.py --test
```
Or, if you've already installed:

```
battery-monitor --test
```

## User Manual

### Auto Start
Every time Battery Monitor starts automatically after PC boots up. It pops up notifications and you see its **Icon** in the system tray. To reveal the other beauties, you can click on the icon. Currently, there are three menus: Settings, About and Quit.

You can also start battery monitor from the menu entries. Please, search for Battery Monitor launcher in the menu entries and simply click on it. In case, if Battery Monitor doesn't start automatically, please open an issue. We would like to debug the issue and help you.

### Settings
In Settings menu, you can configure and adjust settings for Battery Monitor.

#### Configuration
Here, you can set the battery percentage levels at which you want to get notifications. The warning levels are listed in ascending order. **Critical Battery Warning** refers to the lowest level while **First Custom Warning** refers to the highest level. Custom warning levels are optional.

If you change any configuration, it will be in action only after next reboot.

![Battery Monitor GUI](https://github.com/hsbasu/battery-monitor/raw/gh-pages/screenshots/battery-monitor-gui.png)

## Issue Tracking

If you find a bug, to open a new issue with details: [Click Here](https://github.com/hsbasu/battery-monitor/issues)

## Screenshots

#### Initial State

![Initial State](https://github.com/hsbasu/battery-monitor/raw/gh-pages/screenshots/Screenshot_from_2016_07_22_20_42_29.png)

#### Charging State

![Charging State](https://github.com/hsbasu/battery-monitor/raw/gh-pages/screenshots/Screenshot_from_2016_07_22_20_42_52.png)

#### Discharging State

![Discharging State](https://github.com/hsbasu/battery-monitor/raw/gh-pages/screenshots/Screenshot_from_2016_07_22_20_42_42.png)

#### Not Charging State

![Not Charging State](https://github.com/hsbasu/battery-monitor/raw/gh-pages/screenshots/Screenshot_from_2016_07_22_21_11_49.png)

#### Critically Low Battery State

![Critically Low Battery State](https://github.com/hsbasu/battery-monitor/raw/gh-pages/screenshots/Screenshot_from_2016_07_23_03_09_54.png)

## Roadmap

Please take a look at our [milestones](https://github.com/hsbasu/battery-monitor/milestones) to get a clear idea about our roadmap. They are dynamic and they can change frequently on user requests.

## Contributors

### [Himadri Sekhar Basu](https://github.com/hsbasu)

### [Safwan Rahman](https://github.com/safwanrahman)

He has reformatted the code in a new style. The style represents the code easier to understand. Also, he has optimized the code in a way that **Battery Monitor** consumes a little resource of your PC. Please take a minute to thank him.

### [Abdelhak Bougouffa](https://abougouffa.github.io/)

He has fixed some bugs and optimized **Battery Monitor** in a way so that it consumes lower CPU and RAM than before. Please take a minute to thank him.

### [Yochanan Marqos](https://github.com/yochananmarqos)

He is our official package maintainer in AUR. He has put Arch users' life at ease. Please take a minute to thank him.

### [Benjamin Staffin](https://github.com/benley)

He has improved the build process and added modern Python setuptools packaging. Please take a minute to thank him.
