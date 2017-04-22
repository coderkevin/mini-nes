# mini-nes
Support code for my version of a RPi-based Mini NES

This is based on/inspired by [DaftMike's NESPi](http://www.daftmike.com/2016/07/NESPi.html)
It is compatible with the 3D printed parts, but the hardware set up is simplified:

- No Arduino board needed, only the Raspberry Pi
- No power board support (The RPi uses less power than the wall wart you've got plugged in)
- No fan support (buy good heatsinks, you likely won't miss the fan)
- Designed for an RGB LED on the power (for different statuses)

However the following features are (will be) supported

o Power button support
o Reset button support
o RFID Cartidge support
o rsync game library synchronization

I'll update the above list with progress as it goes.
