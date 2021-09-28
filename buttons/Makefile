# Builds nes buttons support code for mini-nes
#

INSTALL_PREFIX := /usr
VAR_WORK_DIR := /var/lib/nes_buttons
INIT_DIR := /etc/init.d

.PHONY: install

install:
	install -m 0755 *.py -D -t $(VAR_WORK_DIR)
	install -m 0755 init/nes_buttons -D -t $(INIT_DIR)
	-systemctl enable nes_buttons
	-systemctl daemon-reload
	-systemctl start nes_buttons

