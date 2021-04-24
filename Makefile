SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
.DEFAULT_GOAL := all

PREFIX ?= /usr
# PREFIX ?= /home/himadri/.local

.PHONY: all
all: install

%.desktop: %.desktop.in
	sed -e 's|%EXEC_PATH%|$(DESTDIR)$(PREFIX)/bin/battery-monitor|' \
            -e 's|%ICON_PATH%|$(DESTDIR)$(PREFIX)/share/pixmaps/battery-monitor.png|' \
            $< > $@

.PHONY: install
install: battery-monitor.desktop battery-monitor-autostart.desktop
	@echo You must be root to install.
	@mkdir -p $(DESTDIR)$(PREFIX)/lib/python3.8/site-packages/
	python3 setup.py install --prefix=$(DESTDIR)$(PREFIX)
	# install -Dm644 battery-monitor-autostart.desktop $(DESTDIR)/etc/xdg/autostart/battery-monitor-autostart.desktop
	install -Dm644 battery-monitor.desktop $(DESTDIR)$(PREFIX)/share/applications/battery-monitor.desktop
	install -Dm644 battery_monitor/icons/icon.png $(DESTDIR)$(PREFIX)/share/pixmaps/battery-monitor.png
	@echo Installation completed!

.PHONY: clean
clean:
	python3 setup.py clean
	rm -rf *.desktop battery_monitor.egg-info build dist
