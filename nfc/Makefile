# Builds nfc support code for mini-nes
#
# Requirements:
#   $NFC_HOME should be set to the libnfc-1.7.1 source directory
#

NFC_INCLUDES = -I$(NFC_HOME) -I$(NFC_HOME)/include

TARGET = nfc_get_uid
LIBS = -lnfc
CC = gcc
CFLAGS = $(NFC_INCLUDES)
OBJECTS = nfc_get_uid.o

.PHONY: default all clean

default: $(TARGET)
all: default

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

.PRECIOUS: $(TARGET) $(OBJECTS)

$(TARGET): $(OBJECTS)
	$(CC) $(OBJECTS) -Wall $(LIBS) -o $@

clean:
	-rm -f $(OBJECTS)
	-rm -f nfc_get_uid

