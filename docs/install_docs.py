#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# rename and install html and manual pages

import os
import sys

PREFIX = os.environ.get('MESON_INSTALL_DESTDIR_PREFIX', '/usr')
src_data = sys.argv[1]
install_dir= os.path.join(PREFIX, sys.argv[2])

if __name__ == '__main__':
	os.makedirs(install_dir, exist_ok=True)
	os.system(f'cp -auv {src_data}/* {install_dir}')
