python_sources = [
  'about_window.py',
	'bm_daemon.py',
	'BMonitor.py',
	'cmd_lines.py',
	'config.py',
	'ErrorLib.py',
	'gui.py',
	'indicator.py',
	'__init__.py',
	'main.py',
	'Notification.py',
]

version_file = configure_file(
  input: 'VERSION.in',
  output: 'VERSION',
  configuration: {
    'version': meson.project_version(),
  }
)

python.install_sources(
  python_sources, version_file,
  subdir: 'BatteryMonitor',
  preserve_path: true,
)

# Install assets like ui and icons
icons = files('icons/charging.png', 'icons/critical-battery.png', 'icons/discharging.png', 'icons/full-charge.png', 'icons/icon.png', 'icons/low-battery.png', 'icons/not-charging.png')

install_data(
  icons,
  install_dir: join_paths(pysrcinstalldir, 'BatteryMonitor', 'icons')
)


ui = files('ui/battery-monitor.ui', 'ui/logger.ui', 'ui/shortcuts.ui',)

install_data(
  ui,
  install_dir: join_paths(pysrcinstalldir, 'BatteryMonitor', 'ui')
)
