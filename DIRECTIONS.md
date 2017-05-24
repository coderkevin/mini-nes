# Mini NES Setup

## Prerequisites

1. Ensure Python 2.7 is working correctly and installed in `/usr/bin/python2.7`
2. `sudo apt-get install python-dev python-pip`

## Enable i2c device
1. `sudo mkdir /etc/nfc`
2. `sudo raspi-config`
3. Select "5 Interfacing"
4. Select "P5 I2C"
5. Select "\<Yes\>"
6. Exit `raspi-config` program
7. `sudo shutdown -r now` to reboot with i2c enabled.

## Install libnfc
1. Ensure you are logged in as `pi` and in the `/home/pi` directory.
2. `wget -O libnfc-1.7.1.tar.bz2 https://bintray.com/nfc-tools/sources/download_file?file_path=libnfc-1.7.1.tar.bz2`
3. `tar -xvf libnfc-1.7.1.tar.bz2`
4. `cd libnfc-1.7.1`
5. `./configure --prefix=/usr --sysconfdir=/etc --with-drivers=pn532_i2c`
6. `make`
7. `sudo make install`
8. After reboot, type `lsmod |grep i2c` and ensure that you see an `i2c_dev` in the list.
9. Also, type `ls /dev/i2c*` and ensure that `/dev/i2c-1` is returned.

## Configure libnfc
1. `sudo nano /etc/nfc/libnfc.conf`
2. Cut and paste the following and save the file.
```
# Allow device auto-detection (default: true)
# Note: if this auto-detection is disabled, user has to manually set a device
# configuration using file or environment variable
allow_autoscan = true

# Allow intrusive auto-detection (default: false)
# Warning: intrusive auto-detection can seriously disturb other devices
# This option is not recommended, so user should prefer to add manually his/her device.
allow_intrusive_scan = false

# Set log level (default: error)
# Valid log levels are (in order of verbosity): 0 (none), 1 (error), 2 (info), 3 (debug)
# Note: if you compiled with --enable-debug option, the default log level is "debug"
log_level = 1

# Manually set default device (no default)
# To set a default device, users must set both name and connstring for their device
# Note: if autoscan is enabled, default device will be the first device available in device list.
device.name = "PN532"
device.connstring = "pn532_i2c:/dev/i2c-1"
```
3. Run `nfc-poll` and ensure you see `NFC reader: pn532_i2c:/dev/i2c-1 opened`
4. Try reading a tag, use Ctrl-C to stop or just wait 30 seconds

## Install nfc_poll
1. Ensure you are logged in as `pi` and in the `/home/pi` directory.
2. `export NFC_HOME=/home/pi/libnfc-1.7.1`
3. `git clone https://github.com/coderkevin/mini-nes.git`
4. `cd mini-nes/nfc`
5. `make`
6. `sudo make install`
7. Run `systemctl status nfc_poll` and ensure you see "Active: active (running)" in the output

## Configure your cartridges

In this system, the cartridges don't need to be written to, we configure a mapping to their UIDs, which should already be uniquely pre-programmed to each tag.

### Record your NFC tag UIDs
1. Run `tail -f /var/log/nfc_poll.log`
2. Place a cartridge (NFC tag) over the reader, the log should output "Reading NFC UID: 00000000000000" where the zeroes are the UID of the tag.
3. Copy/paste the UID into a text file.
4. Continue with all tags you wish to use.

### Record your desired games
1. `cd ~/RetroPie/roms`
2. Start typing `ls <system>/<name of game>` (e.g. `ls nes/Super`) to find the rom you want. Hit tab to complete the file, or hit tab twice to show possible matches. Don't forget to backslash things like spaces and parenthesis as you go.
3. After you finally tab through to the complete file, copy the file name (backslashes and all) and put it next to the UID you want to use in your text file. (`e.g. nes/Super\ Mario\ Bros.\ \(JU\)\ \[\!\].zip`)
5. Repeat this process

### Write your cartridges in the config
1. `sudo nano /etc/nfc_poll/nfc_poll.conf`
2. At the bottom of the file, there's a `[Cartridges]` section.
3. For each cartridge you want, add a line in this format: `<uid> = <game file>` (e.g. `00000000000000 = nes/Super\ Mario\ Bros.\ \(JU\)\ \[\!\].zip`)
4. `sudo systemctl restart nfc_poll`
5. Try it out! Place one of your cartridges on the reader and the screen should go black for a couple seconds, then bring up your game. Remove it and it should go back to the dashboard.

*** Known issue ***
From here, I've got a problem currently. It doesn't seem to recognize joystick inputs for the games that are loaded this way, and pressing any key on the keyboard restarts Emulation Station. I'll continue to work on this, but if you have a solution, contact me!

## Install nes_buttons
1. Ensure you are logged in as `pi` and in the `/home/pi` directory.
2. (If you haven't already) `git clone https://github.com/coderkevin/mini-nes.git`
3. `cd mini-nes/buttons`
4. `sudo make install`
5. Run `systemctl status nes_buttons` and ensure you see "Active: active (running)" in the output
6. From here, you should be able to depress the power button to release it, and the LED should stay lit until the shutdown completes, then turn off. At this point, your RPi CPU is completely off. Now press the power button to latch it, and the RPi should come back up. A reset will simply send a `shutdown -r now` instead and reboot the system.

## Install screen_manager
1. Ensure you are logged in as `pi` and in the `/home/pi` directory.
2. (If you haven't already) `git clone https://github.com/coderkevin/mini-nes.git`
3. `cd mini-nes/screen`
4. `sudo make install`
5. Restart your Pi (try the reset button!) and if you've done all the steps above, everything should be working!

