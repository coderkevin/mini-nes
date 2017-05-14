#!/usr/bin/env python2.7

import sys
import traceback
import log
import logging
import RPi.GPIO as GPIO

# Pin Mappings
RESET_SENSE_PIN = 11
POWER_SENSE_PIN = 13
POWER_HOLD_PIN = 15

class NESButtons():
    def __init__( self, logger ):
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
            callback=self.resetPressed,
            bouncetime=500
            )

    def run( self ):
        GPIO.wait_for_edge( POWER_SENSE_PIN, GPIO.FALLING )
        print( "Power down!" )
        GPIO.cleanup()

    def resetPressed( self, channel ):
        print "Reset!"


if __name__ == "__main__":
    logLevel = logging.DEBUG
    logFormat = '%(asctime)s - $(name)s - %(levelname)s - %(message)s'

    logger = log.initLogger( logLevel, logFormat )

    try:
        app = NESButtons( logger )
        app.run()
    except:
        logger.error( traceback.format_exc() )
        sys.exit(1)

