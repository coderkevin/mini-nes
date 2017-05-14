#!/usr/bin/env python2.7

import sys
import time
import subprocess
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
        self.mode = 'init'

        self.logger.info( "Initializing NES button controls" )

        GPIO.setmode( GPIO.BOARD )
        GPIO.setup( RESET_SENSE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
        GPIO.setup( POWER_SENSE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
        GPIO.setup( POWER_HOLD_PIN, GPIO.OUT )

        # This is the only thing that keeps the RPi alive after the
        # power button is released. We never turn this pin low because
        # the system will hard-reset if we do. We wait for shutdown
        # to take down the GPIO system with it.
        GPIO.output( POWER_HOLD_PIN, GPIO.HIGH )

        self.addHandlers()

    def addHandlers( self ):
        GPIO.add_event_detect(
            RESET_SENSE_PIN,
            GPIO.RISING,
            callback=self.resetPressed,
            bouncetime=500
            )

        GPIO.add_event_detect(
            POWER_SENSE_PIN,
            GPIO.FALLING,
            callback=self.powerPressed,
            bouncetime=500
            )

    def removeHandlers( self ):
        GPIO.remove_event_detect( RESET_SENSE_PIN )
        GPIO.remove_event_detect( POWER_SENSE_PIN )

    def run( self ):
        self.mode = 'run'

        while True:
            time.sleep(5)
            if 'run' != self.mode:
                self.logger.info( "{}ing...".format( self.mode ) )

    def resetPressed( self, channel ):
        self.removeHandlers()
        self.mode = 'restart'
        self.logger.info( "Restarting system..." )
        subprocess.call( "sudo shutdown -r now", shell=True )

    def powerPressed( self, channel ):
        self.removeHandlers()
        self.mode = 'halt'
        self.logger.info( "Powering system down..." )
        subprocess.call( "sudo shutdown -h now", shell=True )

if __name__ == "__main__":
    logLevel = logging.DEBUG
    logFormat = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    logger = log.initLogger( logLevel, logFormat )

    try:
        app = NESButtons( logger )
        app.run()
    except:
        logger.error( traceback.format_exc() )
        sys.exit(1)

