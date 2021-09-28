# Builds nfc support code for mini-nes
#
# Requirements:
#   $NFC_HOME should be set to the libnfc-1.7.1 source directory
#

NFC_INCLUDES := -I$(NFC_HOME) -I$(NFC_HOME)/include

TEST := nfc_get_uid
CC := gcc
CFLAGS := $(NFC_INCLUDES) -fPIC -O3 -g -Wall -Werror
TEST_OBJECTS := nfc_get_uid.o

MAJOR := 0
MINOR := 1
NAME := nfcutils
VERSION := $(MAJOR).$(MINOR)

INSTALL_PREFIX := /usr
VAR_WORK_DIR := /var/lib/nfc_poll
INIT_DIR := /etc/init.d
CONFIG_DIR := /etc/nfc_poll

.PHONY: default all clean lib install

default: $(TEST) lib
all: default

lib: lib$(NAME).so

lib$(NAME).so: lib$(NAME).so.$(VERSION)
	ldconfig -v -n .
	ln -s lib$(NAME).so.$(MAJOR) lib$(NAME).so

lib$(NAME).so.$(VERSION): $(NAME).o
	$(CC) -fPIC -O3 -shared -lnfc -Wl,-soname,lib$(NAME).so.$(MAJOR) $^ -o $@

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

.PRECIOUS: $(TEST) $(TEST_OBJECTS)

$(TEST): $(TEST_OBJECTS) lib$(NAME).so
	$(CC) $(TEST_OBJECTS) -o $@ -L. -l$(NAME) -lnfc

test: $(TEST)
	LD_LIBRARY_PATH=. ./$(TEST) -v

install: lib
	-pip install psutil
	install -m 0755 *.so* -D -t $(INSTALL_PREFIX)/lib
	install -m 0755 *.py -D -t $(VAR_WORK_DIR)
	install -m 0755 init/nfc_poll -D -t $(INIT_DIR)
	install -m 0644 etc/*.conf -D -t $(CONFIG_DIR)
	-systemctl enable nfc_poll
	-systemctl daemon-reload
	-systemctl start nfc_poll

clean:
	-rm -f *.o *.so*
	-rm -f nfc_get_uid

