# Mini NES Power Buttons

This software is designed to work with two buttons:

1. A latching DPDT "Power" switch.
2. A momentary "Reset" switch.

## Reset Switch

This one is easy, it's simply connected to a GPIO and when pressed, the `nes_buttons` daemon issues the `shutdown -r now` command to reboot the system.

## Power Switch

This one is a little trickier. The goal of powering down the system in this way is to ensure as low power usage as possible. For this to happen, the main CPU has to be shut down. That's done easily enough via a `shutdown -h now` command, but in order for the RPi to start back up from that state, the "RUN" pin has to be toggled.

The key part of this system is the RUN pin. This is pin 1 of the RUN header. It sits at 3.3v normally, but if it's pulled down low, it does a hard reset of the RPi. And then it must rise back up to 3.3v for the RPi to start back up.

The theory behind this system is:

 1. A pull-down resistor (10k) is used to pull the RUN pin down by default. This holds the RPi in reset until you push the power button.
 2. When you push the latching power button, it supplies 3.3v to the RUN pin. This brings the RPi out of reset and it boots up.
 3. Upon startup, the `nes_buttons` daemon sets a GPIO to also supply 3.3v to the RUN pin. This ensures the RPi doesn't do a hard reset when you release the latching power button.
 4. When you push the latching power button, it no longer supplies 3.3v to the RUN pin, but the RPi doesn't go into reset because the GPIO is still holding it up to 3.3v. However, the other pins on the power button let the `nes_buttons` daemon know that the power button was released. This runs the `shutdown -h now` command.
 5. The RPi then begins the shutdown process as normal, doing critical things like ensuring all the writes to the SD card are completed (this is why it's bad to pull power on a Pi).
 6. At some point in the shutdown process, the GPIO system is shut down. When this happens, the GPIO that was holding up the RUN pin to 3.3v falls.
 7. Given that there is nothing supplying voltage to the RUN pin, the pull-down resistor takes over and pulls the RUN pin to ground. (on my RPi 3 with a 10k resistor, it is about 0.5v)

