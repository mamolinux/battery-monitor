autostart_dir = join_paths(get_option('sysconfdir'), 'autostart')
desktop_dir = join_paths(datadir, 'applications')
app_icon_dir = join_paths(datadir, 'icons', 'hicolor', 'scalable', 'apps')
schema_dir = join_paths(datadir, 'glib-2.0', 'schemas')
message(f'Autostart dir: @autostart_dir@')
message(f'Desktop file dir: @desktop_dir@')
message(f'Icon dir: @app_icon_dir@')
message(f'Schema dir: @schema_dir@')

# install icon
install_emptydir(app_icon_dir)
install_data(
  join_paths(meson.current_source_dir(), 'icons', f'@application_id@.svg'),
  install_dir: app_icon_dir,
)


# Install desktop file
desktop_file = i18n.merge_file(
        input: 'battery-monitor.desktop.in',
       output: 'battery-monitor.desktop',
         type: 'desktop',
       po_dir: '../po',
      install: true,
  install_dir: desktop_dir
)

# autostart_file = i18n.merge_file(
#         input: 'battery-monitor-autostart.desktop.in',
#        output: 'battery-monitor-autostart.desktop',
#          type: 'desktop',
#        po_dir: '../po',
#       install: true,
#   install_dir: autostart_dir
# )

# Install schema file
schema_file = i18n.merge_file(
        input: 'org.mamolinux.battery-monitor.gschema.xml.in',
       output: 'org.mamolinux.battery-monitor.gschema.xml',
         type: 'xml',
       po_dir: '../po',
      install: true,
  install_dir: schema_dir
)

compile_schemas = find_program('glib-compile-schemas', required: false)
if compile_schemas.found()
  test('Validate schema file',
       compile_schemas,
       args: ['--strict', '--dry-run', meson.current_source_dir()])
endif
