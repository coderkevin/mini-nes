# Installation Instructions



## RetroArch Setup

1. Start up RetroPie
2. Go to the RetroPie Settings
3. Select RetroArch from the menu
4. Go to Settings, Configuration, and set "Save Configuration on Exit" to ON.
5. Go to Network, the Network Commands and set it to ON.
6. Exit RetroArch

## Get SSH connection

The rest of this will be done from your computer for ease.

1. Go to RetroPie Settings
2. Display IP address
3. Log in with SSH on PC using login: pi, password: raspberry

## NFC Setup

Follow instructions here for i2c operation:
https://www.itead.cc/blog/raspberry-pi-drives-itead-pn532-nfc-module-with-libnfc

## Python Setup

4. Copy/paste the following:

```bash
sudo apt-get update
sudo apt-get install python-dev python-pip python-gpiozero
sudo pip install -U nfcpy
```

