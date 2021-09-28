# NES NFC Reader Setup

Full Video & Photo guide will be posted at:                     
http://piwizardgaming.com/nfc                           
                                                                               
For a premade image with all of the below steps already completed visit:       
http://thepiwizard.com  > Select Downloads > and locate the NFC Image Download  

## Step 1 - Prerequisites

1. Download and flash a copy of RetroPie (https://retropie.org.uk/download/) to your SD card And setup your controller.
2. Open the RetroPie menu and then open Raspi-Config
3. Select option `3 Interface Options`
4. Select `P2 SSH` Then select `Yes` to Enable it.  then exit out back to the main menu screen
5. Download Putty On your computer  (https://www.putty.org/)
6. Once installed SSH Into your PI : `Hostname = retropie` Click Open and then `username = pi` `password = raspberry` *Note* It will not display the password as you type it.
7.  Type `python --version` 
      - Ensure Python 2.7 is working correctly and installed in `/usr/bin/python2.7`
8.  Type `sudo apt update`
      - Press `y` when prompted
9.  Type `sudo apt upgrade`
      - Press `y` when prompted
10. Type `sudo apt install python-dev`
      - Press `y` when prompted
11. Type `sudo apt install python-pip`
12. Type `pip --version` 
      - <i>Ensure pip is installed and working (*pip 18.1 from /usr/lib/python2.7/dist-packages/pip (python 2.7)*)</i>
13. Type `sudo pip install python-daemon==2.2.4` 
14. Type `python -m pip install -U pip`
15. Type `pip install watchdog`
16. Type `sudo shutdown -r now` 
17. Once your system reboots - Reconnect with SSH and continue to Step 2

## Step 2 - Enable i2c device
1.  Type `sudo mkdir /etc/nfc`
2.  Type `sudo raspi-config`
3. Select `3 Interfacing`
4. Select `P5 I2C`
5. Select "\<Yes\>"
6. Exit `raspi-config` program
7.  Type `sudo shutdown -r now` to reboot with i2c enabled.
8.  Once your system reboots - Reconnect with SSH and continue to Step 3

## Step 3 - Install libnfc
1. Ensure you are logged in as `pi` and in the `/home/pi` directory.
2.   Type `wget -O libnfc-1.7.1.tar.bz2 https://piwizardgaming.com/nfc/libnfc-1.7.1.tar.bz2`
3.   Type `tar -xvf libnfc-1.7.1.tar.bz2`
4.   Type `cd libnfc-1.7.1`
5.   Type `./configure --prefix=/usr --sysconfdir=/etc --with-drivers=pn532_i2c`
6.   Type `make`
7.   Type `sudo make install`
8.   Type `sudo shutdown -r now`
9.  After reboot, re-open putty and SSH back into the PI and type `lsmod | grep i2c` and ensure that you see an `i2c_dev` in the list.
10. Then type `ls /dev/i2c*` and ensure that `/dev/i2c-1` is returned.

## Step 4 - Configure libnfc
1. Type`cd /etc/nfc`
2. Type`sudo wget http://piwizardgaming.com/nfc/libnfc.conf`
3. Type `nfc-poll` and ensure you see `NFC reader: pn532_i2c:/dev/i2c-1 opened`<br>
![alt text](http://www.piwizardgaming.com/nfc/nfc-poll.png) <br>
4. Try reading a tag, use Ctrl-C to stop or just wait 30 seconds<br>
![alt text](http://www.piwizardgaming.com/nfc/tag-read.png) <br>

## Step 5 - Install nfc_poll
1. Type `cd /home/pi`
2. Type `export NFC_HOME=/home/pi/libnfc-1.7.1`
3. Type `git clone https://github.com/thepiwizard/mini-nes.git`
4. Type `cd mini-nes/nfc`
5. Type `make`
6. Type `sudo make install`
7. Type `systemctl status nfc_poll` and ensure you see "Active: active (running)" in the output<br>
![alt text](http://www.piwizardgaming.com/nfc/status.png) <br>

## Step 6 - Configure your cartridges

In this system, the cartridges don't need to be written to, we configure a mapping to their UIDs, which should already be uniquely pre-programmed to each tag.

## Step 7 - Record your NFC tag UIDs
1.  Type `tail -f /dev/shm/nfc_poll.log`
2. Place a cartridge (NFC tag) over the reader, the log should output "Reading NFC UID: 00000000000000" where the zeroes are the UID of the tag.<br>
![alt text](http://www.piwizardgaming.com/nfc/tag-uid.png) <br>
3. Copy/paste the UID into a text file.
4. Continue with all tags you wish to use.
5. To exit the log, hit \<Ctrl\>-z
 
## Step 8 - Game Download Demo - ###
1. `cd ~/RetroPie/roms/nes`
2. `wget http://piwizardgaming.com/nfc/zelda.zip`

## Step 9 - Write your cartridges in the config
1. `sudo nano /etc/nfc_poll/nfc_poll.conf`
2. At the bottom of the file, there's a `[Cartridges]` section.<br>
![alt text](http://www.piwizardgaming.com/nfc/configure-cart.png) <br>
3. For each cartridge you want, add a line in this format:<br>
     `<uid> = <game file>` (e.g. `00000000000000 = nes/Super Mario Bros. (JU) [!].zip`)<br>
4. If you used the Zelda demo from above simply change the UID in the config file to match yours

## Step 10 - Setup Autostart
1. `sudo nano /etc/rc.local`
2. Scroll down to `exit 0` and press enter twice then copy above the `exit 0` Line
```
sudo systemctl start nfc_poll
sudo systemctl start nes_buttons
```
It should look something like this:<br>
![alt text](http://www.piwizardgaming.com/nfc/rclocal.png) 
 
## Step 11 - Install screen_manager
1.  Type `cd /home/pi/mini-nes/screen`
2.  Type `sudo make install`
  
## Step 12 - Install nes_buttons
1.  Type `cd /home/pi/mini-nes/buttons` 
2.  Type `sudo make install`<br>
![alt text](http://www.piwizardgaming.com/nfc/button-install.png) 
3.  If you have everything wired correctly, your LED should turn on after installing.

## Step 13 - Finish Up ##
1.  Type `sudo shutdown -r now`
2.  Once RetroPie Reboots - Try placing a cartridge on the reader

