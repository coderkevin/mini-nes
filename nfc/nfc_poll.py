#!/usr/bin/env python2.7

from ctypes import *
import sys
import time
import logging

logLevel = logging.DEBUG
logFormat = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

class NFCPoll():
    def __init__( self, logFile = None ):

        self.interval = 5 # seconds
        self.uiPollNr = 1 # number of times to poll each interval
        self.uiPeriod = 1 # nfc polling periods each interval

        self.initLogger( logFile )

        self.libnfc = CDLL("libnfc.so")
        self.libnfcutils = CDLL("libnfcutils.so")

    def initLogger( self, logFile = None ):
        self.logger = logging.getLogger( 'NFCPoll' )
        self.logger.setLevel( logLevel )

        logHandler = None

        if logFile:
            logHandler = logging.FileHandler( logFile )
        else:
            logHandler = logging.StreamHandler( sys.stdout )

        logHandler.setLevel( logLevel )
        logHandler.setFormatter( logging.Formatter( logFormat ) )
        self.logger.addHandler( logHandler )

    def run( self ):
        self.logger.debug( "NFCPoll.run" )
        self.nfc_open()

        self.logger.debug( "Entering main loop" )

        while True:
            uid = self.nfc_poll( self.uiPollNr, self.uiPeriod )

            if uid:
                # TODO: Do something here!
                pass

            time.sleep( self.interval )

    def cleanup( self ):
        self.logger.debug( "cleanup" )
        self.nfc_close()


    def nfc_open( self ):
        res = self.libnfcutils.nfcutils_open()

        if res < 0:
            raise OSError( "Error: Unable to open NFC device: {0}".format( res ) )
        else:
            self.logger.info( "NFC Device Open" )

    def nfc_close( self ):
        res = self.libnfcutils.nfcutils_close()

    def nfc_poll( self, uiPollNr, uiPeriod ):
        charArray20 = c_char * 20
        uidString = charArray20()

        res = self.libnfcutils.nfcutils_poll( uiPollNr, uiPeriod, uidString )

        if res < 0:
            # (KK) On my chipset, it returns a -90 Internal Chip Error when the tag is
            # not present. This sucks as it sounds like a valid error code, but
            # we have to ignore that error as it's a normal condition.
            self.logger.info( "Warning: nfc poll: {0}".format( res ) )
            return None
        elif res == 0:
            self.logger.debug( "No NFC tag found" )
            return None
        elif res == 1:
            self.logger.debug( "NFC tag found: {0}".format( uidString.value ) )
            return uidString.value

if __name__ == "__main__":
    app = NFCPoll()
    app.run()

