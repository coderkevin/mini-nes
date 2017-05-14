# Mini NES Setup

## Prerequisites

1. Ensure Python 2.7 is working correctly and installed in `/usr/bin/python2.7`
2. Ensure you are logged in as `pi` and in the `/home/pi` directory.
3. `wget -O libnfc-1.7.1.tar.bz2 https://bintray.com/nfc-tools/sources/download_file?file_path=libnfc-1.7.1.tar.bz`
4. `tar -xvf libnfc-1.7.1.tar.bz2`
5. `export NFC_HOME=/home/pi/libnfc-1.7.1`

## Install

1. Ensure you are logged in as `pi` and in the `/home/pi` directory.
2. `git clone https://github.com/coderkevin/mini-nes.git`
3. `cd mini-nes/nfc`
4. `make`
5. `sudo make install`

