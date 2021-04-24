NAME=`cat setup.py | grep "name" | cut -d "=" -f 2 | cut -d '"' -f 2`
VERSION=`cat setup.py | grep "version" | cut -d "=" -f 2 | cut -d '"' -f 2`
sed -i "1 i ${NAME} (${VERSION}); urgency=medium" debian/changelog
sed -i '1a\ ' debian/changelog