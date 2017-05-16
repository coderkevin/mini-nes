# Builds nes buttons support code for mini-nes
#

INSTALL_PREFIX := /usr
VAR_WORK_DIR := /var/lib/nes_buttons
INIT_DIR := /etc/init.d

.PHONY: install

install:
	-useradd nes
	-pip install python-daemon
	install -m 0755 *.py -D -t $(VAR_WORK_DIR)
	install -m 0755 init/nes_buttons $(INIT_DIR)
	-systemcfg enable nes_buttons
	-systemcfg daemon-reload

