# Installs screen manager code
#

INSTALL_PREFIX := /usr
VAR_WORK_DIR := /var/lib/screen_manager

.PHONY: install

install:
	-pip install watchdog
	install -m 0755 *.py -D -t $(VAR_WORK_DIR)
	-sh ./update_autostart.sh

