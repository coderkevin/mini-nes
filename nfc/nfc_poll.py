#!/usr/bin/env python2.7

from ctypes import *
import os
import sys
import time
import psutil
import subprocess
import ConfigParser
import traceback
import log
import logging

configDir = '/etc/nfc_poll/'
defaultConfigFile = configDir + 'nfc_poll.conf'

class NFCPoll():
    def __init__( self, options, logger ):

        self.options = options
        self.logger = logger
        self.rom = None

        self.libnfc = CDLL("libnfc.so")
        self.libnfcutils = CDLL("libnfcutils.so")

    def run( self ):
        self.logger.debug( "NFCPoll.run" )
        self.nfc_open()

        self.logger.info( "Entering main loop" )
        self.logger.debug( "cartridges={}".format( self.options['cartridges'] ) )

        while True:
            uid = self.nfc_poll( self.options['uiPollNr'], self.options['uiPeriod'] )
            rom = None

            if uid:
                self.logger.debug( "Reading NFC UID: {}".format( uid ) )
                rom = self.lookupCartridge( uid )

            if rom:
                self.loadRom( rom )
            else:
                self.clearRom()

            time.sleep( self.options['interval'] )

    def loadRom( self, rom ):
        if self.rom != rom:
            self.rom = rom
            system = rom[0:rom.index('/')]
            path = os.path.join( self.options['romsHome'], rom )

            self.writeScreenConfig( [
                "# Action set by nfc_poll",
                "",
                "[Action]",
                "type=rom",
                "system={}".format( system ),
                "path={}".format( path ),
            ] )

    def clearRom( self ):
        if self.rom:
            self.rom = None

            self.writeScreenConfig( [
                "# Action set by nfc_poll",
                "",
                "[Action]",
                "type=dashboard",
            ] )

    def writeScreenConfig( self, lines ):
        with open( self.options['screenConfig'], 'wt' ) as f:
            for line in lines:
                f.write( "{}\n".format( line ) )

    def cleanup( self ):
        self.logger.debug( "cleanup" )
        self.nfc_close()

    def lookupCartridge( self, uid ):
        cartridges = self.options['cartridges']
        if uid in cartridges:
            return cartridges[uid]
        else:
            return None

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
            # (KK) On my chipset, it returns a -104 Internal Chip Error when the tag is
            # not present. This sucks as it sounds like a valid error code, but
            # we have to ignore that error as it's a normal condition.
            self.logger.debug( "Warning: nfc poll: {0}".format( res ) )
            return None
        elif res == 0:
            self.logger.debug( "No NFC tag found" )
            return None
        elif res == 1:
            self.logger.debug( "NFC tag found: {0}".format( uidString.value ) )
            return uidString.value

def initConfig( logger, configFile = defaultConfigFile ):
    config = ConfigParser.RawConfigParser()
    config.read( configFile )

    cartridgeIds = config.options( 'Cartridges' )
    cartridges = {}

    for uid in cartridgeIds:
        cartridges[ uid ] = config.get( 'Cartridges', uid )

    return {
        'romsHome': config.get( 'Settings', 'roms_home' ),
        'screenConfig': config.get( 'Settings', 'screen_config_file' ),
        'interval': config.getint( 'Settings', 'interval_seconds' ),
        'uiPollNr': config.getint( 'Settings', 'ui_poll_nr' ),
        'uiPeriod': config.getint( 'Settings', 'ui_period' ),
        'cartridges': cartridges
    }

if __name__ == "__main__":
    logLevel = logging.DEBUG
    logFormat = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    logger = log.initLogger( logLevel, logFormat )

    try:
        options = initConfig( logger )

        app = NFCPoll( options, logger )
        app.run()
    except:
        logger.error( traceback.format_exc() )
        sys.exit(1)

