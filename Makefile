#####################################################################################
# Copyright 2019 Normation SAS
#####################################################################################
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, Version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#####################################################################################

.DEFAULT_GOAL := build

RUDDER_VERSION_TO_PACKAGE =
RUDDER_MAJOR_VERSION := $(shell echo ${RUDDER_VERSION_TO_PACKAGE} | cut -d'.' -f 1-2)

DESTDIR = $(CURDIR)/target

build:
	cd lib.python && ./build.sh

# Install into DESTDIR
install: build
	# Directories
	mkdir -p $(DESTDIR)/usr/bin/
	mkdir -p $(DESTDIR)/usr/share/rudder-api-client/

	# Install python lib
	install -m 755 lib.python/rudder.py $(DESTDIR)/usr/share/rudder-api-client/rudder.py
	# Install cli exec
	install -m 755 cli/rudder-cli $(DESTDIR)/usr/bin/rudder-cli

# Clean

clean:
	rm -rf target
	cd lib.python && ./clean.sh

veryclean: clean
distclean: veryclean
localclean: clean
localdepends:

.PHONY: localdepends localclean veryclean
