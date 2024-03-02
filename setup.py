import glob
import os
import subprocess

from setuptools import setup
from subprocess import check_output

for line in check_output('dpkg-parsechangelog --format rfc822'.split(),
                         universal_newlines=True).splitlines():
    header, colon, value = line.lower().partition(':')
    if header == 'version':
        version = value.strip()
        break
else:
    raise RuntimeError('No version found in debian/changelog')

with open("src/BatteryMonitor/VERSION", "w") as f:
    if '~' in version:
        version = version.split('~')[0]
    f.write("%s" % version)

gschema_dir_suffix = 'share/glib-2.0/schemas'

data_files = [('share/applications', glob.glob("data/applications/*.desktop")),
			('share/icons/hicolor/scalable/apps', glob.glob("data/icons/*")),
			(gschema_dir_suffix, glob.glob("data/schema/*.xml"))
			]

def create_mo_files():
	po_files = glob.glob("po/*.po")
	prefix = 'battery-monitor'
	
	for po_file in po_files:
		po_name = os.path.splitext(os.path.split(po_file)[1])[0]
		replace_txt = "%s-" % prefix
		lang = po_name.replace(replace_txt, '')
		os.makedirs("data/locale/%s" % lang, exist_ok=True)
		mo = "data/locale/%s/%s.mo" % (lang, prefix)
		subprocess.run(['msgfmt', '-o', str(mo), po_file], check=True)
		
		mo_file = map(lambda i: ('share/locale/%s/LC_MESSAGES' % lang, [i+'/%s.mo' % prefix]), glob.glob('data/locale/%s' % lang))
		data_files.extend(mo_file)

create_mo_files()

setup(data_files=data_files,
		# cmdclass = {'install_data': install_data}
)
