project('battery-monitor',
  version: run_command('head', '-1', 'debian/changelog', check: true).stdout().split(' ')[1].strip('(').strip(')'),
  default_options: ['warning_level=3',
    'prefix=/usr',
  ]
)


i18n = import('i18n')
gnome = import('gnome')
pymod = import('python')
python = pymod.find_installation('python3')
gettext_package = meson.project_name()

# dependency('gobject')
# dependency('bs4')
# dependency('configobj')

datadir = get_option('datadir')

subdir('data')
subdir('po')
subdir('src')

gnome.post_install(
     glib_compile_schemas: true,
    gtk_update_icon_cache: true,
  update_desktop_database: true,
)
