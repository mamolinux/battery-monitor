# [Battery Monitor](https://hsbasu.github.io/battery-monitor)

<p align="center">
	<img src="https://raw.githubusercontent.com/mamolinux/battery-monitor/master/data/icons/battery-monitor.svg?sanitize=true" height="128" alt="Logo">
</p>

<p align="center">
	<a href="#">
		<img src="https://img.shields.io/github/actions/workflow/status/mamolinux/battery-monitor/ci.yml?branch=master&label=CI%20Build" alt="CI build">
	</a>
	<a href="#">
		<img src="https://img.shields.io/github/actions/workflow/status/mamolinux/battery-monitor/codeql-analysis.yml?branch=master&label=CodeQL%20Build" alt="CodeQL build">
	</a>
	<a href="https://github.com/mamolinux/battery-monitor/blob/master/LICENSE">
		<img src="https://img.shields.io/github/license/mamolinux/battery-monitor?label=License" alt="License">
	</a>
	<a href="#">
		<img src="https://img.shields.io/github/repo-size/mamolinux/battery-monitor?label=Repo%20size" alt="GitHub repo size">
	</a>
	<a href="https://github.com/mamolinux/battery-monitor/releases/latest">
		<img src="https://img.shields.io/github/v/release/mamolinux/battery-monitor?label=Latest%20Stable%20Release" alt="GitHub release (latest by date)">
	</a>
	<a href="https://github.com/mamolinux/battery-monitor/issues" target="_blank">
		<img src="https://img.shields.io/github/issues/mamolinux/battery-monitor?label=Issues" alt="Open Issues">
	</a>
	<a href="https://github.com/mamolinux/battery-monitor/pulls" target="_blank">
		<img src="https://img.shields.io/github/issues-pr/mamolinux/battery-monitor?label=PR" alt="Open PRs">
	</a>
	<a href="#download-latest-version">
		<img src="https://img.shields.io/github/downloads/mamolinux/battery-monitor/total?label=Downloads" alt="Downloads">
	</a>
	<a href="https://github.com/mamolinux/battery-monitor/releases/download/1.1.2/battery-monitor_1.1.2_all.deb">
		<img src="https://img.shields.io/github/downloads/mamolinux/battery-monitor/1.1.2/battery-monitor_1.1.2_all.deb?label=Downloads%40Latest%20Binary" alt="GitHub release (latest by date and asset">
	</a>
</p>

Many a times we forget to remove the laptop charger. This can reduce the battery life significantly due to overcharging. This is where Battery Monitor comes into play.

Battery Monitor is a utility tool developed on Python3 and PyGtk3. It will notify the user about charging, discharging, not charging and critically low state of the battery on Linux (surely if the battery is present). Along with showing the notification repetitively, It also plays a sound so that you don't miss the notification.

## Download Latest Version
<p align="center">
	<a href="https://github.com/mamolinux/battery-monitor/zipball/master">Download Source (.zip)</a></br>
	<a href="https://github.com/mamolinux/battery-monitor/tarball/master">Download Source (.tar.gz)</a></br>
	<a href="https://github.com/mamolinux/battery-monitor/releases/download/1.1.2/battery-monitor_1.1.2_all.deb">Download Binary (.deb)</a>
</p>

## Features and Screenshots
Battery Monitor notifies the user:
1. Whether [battery is present](#initial-state),
2. When charger is [plugged in](#charging-state),
3. When charger is [unplugged](#discharging-state),
4. When battery is [full and charger is not unplugged](#not-charging-state),
5. When battery is [critically low](#critically-low-battery-state).

Additionally, it can show notifications:
1. At three user-defined battery percentage during discharging,
2. At one user-defined battery percentage during charging,
3. Along with playing a sound (Mute option is not available yet).

#### Initial State

<p align="center">
	<img src="https://github.com/mamolinux/battery-monitor/raw/gh-pages/screenshots/initial-state.png" alt="Initial State">
</p>

#### Charging State

<p align="center">
	<img src="https://github.com/mamolinux/battery-monitor/raw/gh-pages/screenshots/charging.png" alt="Charging State">
</p>

#### Discharging State

<p align="center">
	<img src="https://github.com/mamolinux/battery-monitor/raw/gh-pages/screenshots/discharging.png" alt="Discharging State">
</p>

#### Not Charging State

<p align="center">
	<img src="https://github.com/mamolinux/battery-monitor/raw/gh-pages/screenshots/not-charging.png" alt="Not Charging State">
</p>

#### Critically Low Battery State

<p align="center">
	<img src="https://github.com/mamolinux/battery-monitor/raw/gh-pages/screenshots/critically-low.png" alt="Critically Low Battery State">
</p>

### Settings Window
In Settings menu, you can configure and adjust settings for Battery Monitor. Here, you can set the battery percentage levels at which you want to get notifications. The warning levels are listed in ascending order. **Critical Battery Warning** refers to the lowest level while **First Custom Warning** refers to the highest level. Custom warning levels are optional.

**N.B.** If you change any configuration, it will be in action only after next reboot.
<p align="center">
	<img src="https://github.com/mamolinux/battery-monitor/raw/gh-pages/screenshots/settings-window.png" alt="Battery Monitor GUI">
</p>

## Contents
- [Download Latest Version](#download-latest-version)
- [Features and Screenshots](#features-and-screenshots)
- [Dependencies](#dependencies)
	- [Debian/Ubuntu based systems](#debianubuntu-based-distro)
	- [Other Linux-based systems](#other-linux-based-distro)
- [Installation](#build-and-install-the-latest-version)
	- [Debian/Ubuntu based systems](#debianubuntu-based-systems)
	- [Other Linux-based systems](#other-linux-based-systems)
	- [For Developers](#for-developers)
- [User Manual](#user-manual)
	- [Auto Start](#auto-start)
- [Issue Tracking and Contributing](#issue-tracking-and-contributing)
- [Contributors](#contributors)

## Dependencies
```
acpi
python3
python3-gi
python3-setuptools
libnotify4
libappindicator3-1
gir1.2-appindicator3-0.1
```
To use or test **Battery Monitor**, you need these dependencies to be installed.

### Debian/Ubuntu based distro
To install dependencies on Debian/Ubuntu based systems, run:
```
sudo apt install acpi python3 python3-gi python3-setuptools \
libnotify4 libappindicator3-1 gir1.2-appindicator3-0.1
```
**Note**: If you are using `gdebi` to install **Battery Monitor** from a `.deb` file, it will automatically install the dependencies and you can skip this step.

### Other Linux-based distro
Remove `apt install` in the command given in [Debian/Ubuntu based distros](#debianubuntu-based-distro) and use the command for the package manager of the target system(eg. `yum install`, `dnf install`, `pacman -S` etc.)

**Note**: There might be cases where one or more dependencies might not be available for your system. But that is highly unlikely. In such situations, please [create an issue](#issue-tracking-and-contributing).

## Build and Install the Latest Version

### Debian/Ubuntu based systems
There are two methods, this app can be installed/used on a Debian/Ubuntu based system. First, download and unzip the source package using:
```
wget https://github.com/mamolinux/battery-monitor/archive/refs/heads/master.zip
unzip master.zip
cd battery-monitor-master
```

1. **Option 1:** Manually copying necessary files to root (`/`). For that, follow the steps below:
	1. [**Optional**] To make translations/locales in languages other than **English**, run:
		```
		make
		```
		from the `battery-monitor-master` in a terminal. It will create the translations/locales in `usr/share/locale`.

	2. Copy the contents of `usr/` to `/usr/`:
		```
		sudo cp -R usr /
		```
	3. Copy the contents of `etc/` to `/etc/`:
		```
		sudo cp -R etc /
		```
	4. Compile `schemas` using:
		```
		sudo glib-compile-schemas /usr/share/glib-2.0/schemas
		```

2. **Option 2:** Build a debian package and install it. To build a debian package on your own:
	1. After using `cd battery-monitor-master`, run:
		```
		dpkg-buildpackage --no-sign
		```
		This will create a `battery-monitor_*.deb` package at `../battery-monitor-master`.
		
	2. Install the debian package using
		```
		sudo dpkg -i ../battery-monitor_*.deb
		sudo apt install -f
		```
After it is installed, run `battery-monitor` from terminal or use the `battery-monitor.desktop`.

### Other Linux-based systems
1. Install the [dependencies](#other-linux-based-distro).
2. From instructions for [Debian/Ubuntu based systems](#debianubuntu-based-systems), follow **Option 1**.

### For Developers
If you want to test **Battery Monitor**,
1. Get the source package and unzip it using:
	```
	wget https://github.com/mamolinux/battery-monitor/archive/refs/heads/master.zip
	unzip master.zip
	cd battery-monitor-master/usr/lib/battery-monitor
	```
2. Then run:
	```
	python3 battery-monitor.py --test
	```
	Or, if you've already installed:
	
	```
	battery-monitor --test
	```

**I have no knowledge on how to use `meson` or `npm` for testing. If you can offer any help regarding this, please start a discussion [here](https://github.com/mamolinux/battery-monitor/discussions) or create a [PR](https://github.com/mamolinux/battery-monitor/compare). It will be more than welcome.**

## User Manual

### Auto Start
Every time Battery Monitor starts automatically after PC boots up. It pops up notifications and you see its **Icon** in the system tray. To reveal the other beauties, you can click on the icon. Currently, there are three menus: **Settings**, **About** and **Quit**.

You can also start battery monitor from the menu entries. Please, search for Battery Monitor launcher in the menu entries and simply click on it. In case, if Battery Monitor doesn't start automatically, please open an [issue](#issue-tracking-and-contributing). We would like to debug the issue and help you.

## Issue Tracking and Contributing
If you are interested to contribute and enrich the code, you are most welcome. You can do it by:
1. If you find a bug, to open a new issue with details: [Click Here](https://github.com/mamolinux/battery-monitor/issues)
2. If you know how to fix a bug or want to add new feature/documentation to the existing package, please create a [Pull Request](https://github.com/mamolinux/battery-monitor/compare).

**NB:** Using the issue template or PR template is **not** mandatory.

## Contributors

### [Himadri Sekhar Basu](https://hsbasu.github.io)
Current maintainer.

### [Maksudur Rahman Maateen](https://github.com/maateen)
He is the original creator of now archived [Battery Monitor](https://github.com/maateen/battery-monitor). We are highly grateful to him for offering this useful app and providing the base for the current [Battery Monitor](https://github.com/mamolinux/battery-monitor). Please take a minute to thank him.

### [Safwan Rahman](https://github.com/safwanrahman)

He has reformatted the code in a new style. The style represents the code easier to understand. Also, he has optimized the code in a way that **Battery Monitor** consumes a little resource of your PC. Please take a minute to thank him.

### [Abdelhak Bougouffa](https://abougouffa.github.io/)

He has fixed some bugs and optimized **Battery Monitor** in a way so that it consumes lower CPU and RAM than before. Please take a minute to thank him.

### [Yochanan Marqos](https://github.com/yochananmarqos)

He is our official package maintainer in AUR. He has put Arch users' life at ease. Please take a minute to thank him.

### [Benjamin Staffin](https://github.com/benley)

He has improved the build process and added modern Python setuptools packaging. Please take a minute to thank him.

## Donations
I am a freelance programmer. So, If you like this app and would like to offer me a coffee ( &#9749; ) to motivate me further, you can do so via:

[![](https://liberapay.com/assets/widgets/donate.svg)](https://liberapay.com/hsbasu/donate)
[![](https://www.paypalobjects.com/webstatic/i/logo/rebrand/ppcom.svg)](https://paypal.me/hsbasu)
[![](https://hsbasu.github.io/styles/icons/logo/svg/upi-logo.svg)](https://hsbasu.github.io/images/upi-qr.jpg)
