# RetroPie Screen Manager

This is a script that manages what shows on the screen for RetroPie.
It is installed in place of emulationstation, and provides a system-level
way of starting roms or emulationstation.

# Installation

After cloning the repo, simply cd to this directory and run `sudo make install`.
This will copy the script to `/var/lib/screen_manager` and embed it into the
RetroPie autostart script. (`/opt/retropie/config/all/autostart.sh`)

# Operation

On startup, the `screen_manager.py` script will be run instead of `emulationstation`.
However, default action is to run `emulationstation`, so if you have no config file,
it will look the same as before.

## Configuration File

This script looks for a configuration file at `/dev/shm/screen_manager.cfg`

The `screen_manager.py` script actively watches this file, so as soon as the file
is written, the script will respond and run the action. If the parsing of the file
ends up with an identical action as before, the action will be ignored. (so it's
okay to write the same action to it multiple times.)

This script and configuration file is designed to work with other system processes such as:
  - A daemon that monitors GPIOs for button presses, then starts a rom.
  - An nfc reader daemon that watches for a tag and starts a rom, then runs the dashboard after the tag is removed.

All you have to do is handle your input the way you need to, and then write the
config file in response.

For an example, look at my [NFC Poll Daemon](https://github.com/coderkevin/mini-nes/tree/master/nfc)

The existing code for this script handles two action types by default (although you can add more!)

### dashboard (emulationstation)

This action type simply runs emulationstation.
```
[Action]
type=dashboard
```

### rom

This action uses `runcommand` to start a rom with the appropriate emulator.
```
[Action]
type=rom
system=<console name (e.g. nes)>
path=<absolute path to rom (e.g. /home/pi/RetroPie/roms/nes/myrom.zip)>
```

# Logging

A log for the script is kept at `/dev/shm/screen_manager.log`
Log level can be modified by editing the script itself (at `/var/lib/screen_manager/screen_manager.py`)

# Known Limitations

- If after running an action, the process exits, no further action will be taken by this script. The most likely scenario for this is exiting RetroArch by hitting `[select]+[start]` In that case, the user will see the console and a different action must be run.

