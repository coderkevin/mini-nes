# Mini NES Troubleshooting Guide

Things not working the way they should? Check here for some tactics on diagnosing your problem.

## Power Buttons

### Software

- Program: `nes_buttons` daemon (should be running on system startup)
- How to start: `sudo systemctl start nes_buttons`
- How to stop: `sudo systemctl stop nes_buttons`
- How to check the log: `cat /dev/shm/nes_buttons.log`

If the system daemon isn't behaving the way you'd expect, you can run the code manually.

1. `sudo systemctl stop nes_buttons`
2. Change your directory to the `buttons` subdirectory of the source.
3. `python nes_buttons.py`
4. Logging output should be visible on the command line. (If you see a "RuntimeWarning" about a channel already in use, that's okay.)
5. Press the reset button. You should see logging output about restarting.

### Electrical

If your power isn't shuttting down and starting back up correctly, here are a couple things to check:

1. Ensure the power button is unlatched and then plug in the RPi power.
2. Use a multimeter to test for voltage on RUN pin #1. It should be around 0.5v or less.
3. Press the power button to latch it.
4. The LED should turn on, indicating that RUN pin #1 has risen in voltage.
5. The system should power up as normal.

If your RPi turns off but not back on, it's likely because the RUN pin isn't pulled low enough before rising back to 3.3v. On my RPi 3, a 10k is enough to drop the RUN pin to 0.5v. Check with a multimeter when the device is plugged in, but the power button is not on. If it's too high, then try a lower value resistor. Something between 10k down to 1k should work. When you try out a different resistor, test the voltage, then try the behavior.


## NFC Reader

### Software

- Program: `nfc_poll` daemon (should be running on system startup)
- How to start: `sudo systemctl start nfc_poll`
- How to stop: `sudo systemctl stop nfc_poll`
- How to check the log: `cat /dev/shm/nfc_poll.log`

If the system daemon isn't behaving the way you'd expect, you can run the code manually.

1. `sudo systemctl stop nfc_poll`
2. Change your directory to the `nfc` subdirectory of the source.
3. `python nfc_poll.py`
4. Logging output should be visible on the command line.
5. Try placing a cartridge over the sensor and watch for output.

### Electrical

If your nfc reader isn't working correctly, it should show up in the logs. If you suspect it's electrical, here are some things to check:

1. There are two small DIP switches on the NFC board to select the mode. Ensure they're set correctly for i2c.
2. Ensure the correct pins are connected to the RPi header and the NFC board. Revisit the wiring diagram for this.
3. The red LED on the NFC board should be on any time the RPi header is plugged in.


## Screen Manager

### Software

- Script: `/var/lib/screen_manager/screen_manager.py` (called by autostart.sh)
- How to check the log: `cat /dev/shm/screen_manager.log`

This script should be fairly stable and shouldn't have too many problems. If emulationstation is running on startup, then this script is running.

The installation for this script modifies `/opt/retropie/configs/all/autostart.sh`. It comments out emulationstation and adds `python screen_manager.py` instead. If this is causing problems, you can edit this file and restore default operation there.

You can run this script manually just like the others, but you'll want to disable it in `autostart.sh` before you do.

To test:

1. Edit the config file at `cat /dev/shm/screen_manager.cfg` in accordance with [the screen readme](https://github.com/coderkevin/mini-nes/blob/master/screen/README.md)
2. Try a `dashboard` action.
3. Try a `rom` action.
4. Try deleting the file to ensure the default dashboard action runs.



