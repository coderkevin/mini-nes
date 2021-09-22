# Mini NES Setup

## Step 1 - Prerequisites

1. Download and flash a copy of RetroPie (https://retropie.org.uk/download/) to your SD card And setup your controller.
2. Open the RetroPie menu and then open Raspi-Config
3. Select option `3 Interface Options`
4. Select `P2 SSH` Then select `Yes` to Enable it.  then exit out back to the main menu screen
5. Download Putty On your computer  (https://www.putty.org/)
6. Once installed SSH Into your PI : `Hostname = retropie` Click Open and then `username = pi` `password = raspberry` *Note* It will not display the password as you type it.
7.  Type `python --version` Ensure Python 2.7 is working correctly and installed in `/usr/bin/python2.7`
8.  Type `sudo apt update`
9.  Type `sudo apt upgrade`
10. Type `sudo apt install python-dev`
11. Type `sudo apt install pyton-pip`
12. Type `pip --version` Ensure pip is installed and working (*pip 18.1 from /usr/lib/python2.7/dist-packages/pip (python 2.7)*)
13. Type `sudo pip install python-daemon==2.2.4` 
14. Type `python -m pip install -U pip`
15. Type `pip install watchdog`

## Step 2 - Enable i2c device
1.  Type `sudo mkdir /etc/nfc`
2.  Type `sudo raspi-config`
3. Select `3 Interfacing`
4. Select `P5 I2C`
5. Select "\<Yes\>"
6. Exit `raspi-config` program
7.  Type `sudo shutdown -r now` to reboot with i2c enabled.

## Step 3 - Install libnfc
1. Re-open putty and SSH back into your PI
2. Ensure you are logged in as `pi` and in the `/home/pi` directory.
3.  Type `wget -O libnfc-1.7.1.tar.bz2 https://piwizardgaming.com/nfc/libnfc-1.7.1.tar.bz2`
3.  Type `tar -xvf libnfc-1.7.1.tar.bz2`
4.  Type `cd libnfc-1.7.1`
5.  Type `./configure --prefix=/usr --sysconfdir=/etc --with-drivers=pn532_i2c`
6.  Type `make`
7.  Type `sudo make install`
8.  Type `sudo shutdown -r now`
9. After reboot, re-open putty and SSH back into the PI and type `lsmod | grep i2c` and ensure that you see an `i2c_dev` in the list.
10.Then type `ls /dev/i2c*` and ensure that `/dev/i2c-1` is returned.

## Step 4 - Configure libnfc
1. Type`cd /etc/nfc`
2. Type`sudo wget http://piwizardgaming.com/nfc/libnfc.conf`
3. Type `nfc-poll` and ensure you see `NFC reader: pn532_i2c:/dev/i2c-1 opened`
4. Try reading a tag, use Ctrl-C to stop or just wait 30 seconds

## Step 5 - Install nfc_poll
1. Type `cd /home/pi`
2. Type `export NFC_HOME=/home/pi/libnfc-1.7.1`
3. Type `git clone https://github.com/thepiwizard/mini-nes.git`
4. Type `cd mini-nes/nfc`
5. Type `make`
6. Type `sudo make install`
7. Run `systemctl status nfc_poll` and ensure you see "Active: active (running)" in the output

## Step 6 - Configure your cartridges

In this system, the cartridges don't need to be written to, we configure a mapping to their UIDs, which should already be uniquely pre-programmed to each tag.

### Step 7 - Record your NFC tag UIDs
1. Run `tail -f /dev/shm/nfc_poll.log`
2. Place a cartridge (NFC tag) over the reader, the log should output "Reading NFC UID: 00000000000000" where the zeroes are the UID of the tag.
3. Copy/paste the UID into a text file.
4. Continue with all tags you wish to use.
5. To exit the log, hit \<Ctrl\>-C

### Step 8 - Record your desired games
1. `cd ~/RetroPie/roms`
2. Start typing `ls <system>/<name of game>` (e.g. `ls nes/Super`) to find the rom you want. Hit tab to complete the file, or hit tab twice to show possible matches. Don't forget to backslash things like spaces and parenthesis as you go.
3. After you finally tab through to the complete file, hit <enter>.
4. Copy the resulting line and put it and put it next to the UID you want to use in your text file. (`e.g. nes/Super Mario Bros. (JU) [!].zip`) Make sure you don't have backslashes here.
5. Repeat this process
  
### Step 9 - Game Download Demo ###
1. `cd ~/RetroPie/roms/nes`
2. `wget http://piwizardgaming.com/nfc/1942.zip`

### Step 10 - Write your cartridges in the config
1. `sudo nano /etc/nfc_poll/nfc_poll.conf`
2. At the bottom of the file, there's a `[Cartridges]` section.
3. For each cartridge you want, add a line in this format: `<uid> = <game file>` (e.g. `00000000000000 = nes/Super Mario Bros. (JU) [!].zip`)

## Step 11 - Setup Autostart
1. `sudo nano /etc/rc.local`
2. Scroll down to `exit 0` and press enter twice then copy above the `exit 0` Line
```
sudo systemctl start nfc_poll
sudo systemctl start nes_buttons
```
It should look something like this:<br>
![alt text](http://www.piwizardgaming.com/nfc/rclocal.png) 
 
## Step 12 - Install screen_manager
1.  Type `cd mini-nes/screen`
2.  Type `sudo make install`
  
## Step 13 - Install nes_buttons
1.  Type `cd /home/pi` 
2.  Type `cd mini-nes/buttons`
3.  Type `sudo make install`

## Step 14 - Finish Up ##
1.  Type `sudo shutdown -r now`
2.  Once RetroPie Reboots - Try placing a cartridge on the reader

## Full Video & Photo guide will be posted at:
http://piwizardgaming.com/nfc 
