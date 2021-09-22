# Mini NES Setup

## Prerequisites

1. `python --version` Ensure Python 2.7 is working correctly and installed in `/usr/bin/python2.7`
2. `sudo apt update`
3. `sudo apt upgrade`
4. `sudo apt-get install python-dev`
5. `sudo apt-get install pyton-pip`
6. `pip --version` Ensure pip is installed and working
7. `sudo pip install python-daemon==2.2.4` 

## Enable i2c device
1. `sudo mkdir /etc/nfc`
2. `sudo raspi-config`
3. Select "3 Interfacing"
4. Select "P5 I2C"
5. Select "\<Yes\>"
6. Exit `raspi-config` program
7. `sudo shutdown -r now` to reboot with i2c enabled.

## Install libnfc
1. Ensure you are logged in as `pi` and in the `/home/pi` directory.
2. `wget -O libnfc-1.7.1.tar.bz2 https://piwizardgaming.com/nfc/libnfc-1.7.1.tar.bz2`
3. `tar -xvf libnfc-1.7.1.tar.bz2`
4. `cd libnfc-1.7.1`
5. `./configure --prefix=/usr --sysconfdir=/etc --with-drivers=pn532_i2c`
6. `make`
7. `sudo make install`
8. `sudo shutdown -r now`
9. After reboot, type `lsmod | grep i2c` and ensure that you see an `i2c_dev` in the list.
10. Also, type `ls /dev/i2c*` and ensure that `/dev/i2c-1` is returned.

## Configure libnfc
1. `cd /etc/nfc`
2. `sudo wget http://piwizardgaming.com/nfc/libnfc.conf`
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
1. Run `tail -f /dev/shm/nfc_poll.log`
2. Place a cartridge (NFC tag) over the reader, the log should output "Reading NFC UID: 00000000000000" where the zeroes are the UID of the tag.
3. Copy/paste the UID into a text file.
4. Continue with all tags you wish to use.
5. To exit the log, hit \<Ctrl\>-C

### Record your desired games
1. `cd ~/RetroPie/roms`
2. Start typing `ls <system>/<name of game>` (e.g. `ls nes/Super`) to find the rom you want. Hit tab to complete the file, or hit tab twice to show possible matches. Don't forget to backslash things like spaces and parenthesis as you go.
3. After you finally tab through to the complete file, hit <enter>.
4. Copy the resulting line and put it and put it next to the UID you want to use in your text file. (`e.g. nes/Super Mario Bros. (JU) [!].zip`) Make sure you don't have backslashes here.
5. Repeat this process
  
### Game Download Demo ###
1. `cd ~/RetroPie/roms/nes`
2. `wget http://piwizardgaming.com/nfc/1942.zip`

### Write your cartridges in the config
1. `sudo nano /etc/nfc_poll/nfc_poll.conf`
2. At the bottom of the file, there's a `[Cartridges]` section.
3. For each cartridge you want, add a line in this format: `<uid> = <game file>` (e.g. `00000000000000 = nes/Super Mario Bros. (JU) [!].zip`)
4. `sudo systemctl restart nfc_poll`
5. Try it out! Place one of your cartridges on the reader and the screen should go black for a couple seconds, then bring up your game. Remove it and it should go back to the dashboard.

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

## Setup Autostart ##
1. `sudo nano /etc/rc.local`
2. Scroll down to `exit 0` and press enter twice then copy above the `exit 0` Line
```
sudo systemctl start nfc_poll
sudo systemctl start nes_buttons
```
It should look something like this: http://www.piwizardgaming.com/nfc/rclocal.png 
## Finish Up ##
1. `sudo shutdown -r now`
2.  Try placing a cartridge on the reader
  
