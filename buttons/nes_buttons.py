#!/usr/bin/env python2.7

import sys
import RPi.GPIO as GPIO

# Pin Mappings
RESET_SENSE_PIN = 17
POWER_SENSE_PIN = 27
POWER_HOLD_PIN = 22

class NESButtons():
    def __init__( self, options ):
        self.logger = logger

        GPIO.setmode( GPIO.BOARD )
        GPIO.setup( RESET_SENSE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
        GPIO.setup( POWER_SENSE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
        GPIO.setup( POWER_HOLD_PIN, GPIO.OUT )

        # This is the only thing that keeps the RPi alive after the
        # power button is released
        GPIO.output( POWER_HOLD_PIN, GPIO.HIGH )

        GPIO.add_event_detect(
            RESET_SENSE_PIN,
            GPIO.RISING,
            callback=this.resetPressed,
            bouncetime=300
            )

        GPIO.add_event_detect(
            POWER_SENSE_PIN,
            GPIO.FALLING,
            callback=this.powerReleased,
            bouncetime=300
            )

    def resetPressed( self ):
        print "Reset!"

    def powerReleased( self ):
        print "Power Released!"



