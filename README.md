# mini-nes
Support code for my version of a RPi-based Mini NES

This is based on/inspired by [DaftMike's NESPi](http://www.daftmike.com/2016/07/NESPi.html)
It is compatible with the 3D printed parts, but the hardware set up is simplified:

- No Arduino board needed, only the Raspberry Pi
- No power board support (In CPU shutdown, the RPi uses less power than the USB power supply you're using to power it)
- No fan support (buy good heatsinks, you likely won't miss the fan)

Here's a more detailed list of the features:

## Latching Power Button

The Power button is handled via GPIO and reset pin on the RPi.
The power button, when latched, brings the reset pin high, awakening the RPi from its shutdown.
After the RPi is powered up, a script is used on an output GPIO pin to hold the reset pin high in addition to the power button.
When the power button is unlatched, the GPIO holds the reset pin high until system shutdown completes.

## Power LED

The Power LED is connected to the reset pin, this indicates the true run state of the RPi. If the reset pin is high, the RPi is running. If the reset pin is low, then the RPi is held in reset and the CPU is in shutdown. It looks a little strange to see the power LED remain lit for a few seconds after unlatching the power button, but it is reassuring to know that the RPi isn't being subjected to a hard reset.

## Reset Button

The Reset button is connected to an RPi GPIO and simply does a system reboot.

## NFC Cartidge support

The NFC Reader is a PN532 running on the RPi's i2c interface. I've made a simple c interface to Python to utilize it. No Arduino or microcontroller needed to use it.

## No NFC tag writing needed

This system is designed to simply rely on the unique IDs already imprinted on your NFC tags. It uses a configuration file to map those UIDs to the correct game files to be run.

## Immediate loading of games

The system doesn't have to be powered off to start a game. It continually scans for cartridges and will restart Emulation Station as soon as a cart is installed. Don't worry if you like the feel of the old process though. You can still power off the system and install your cart and power it back on if you like.

