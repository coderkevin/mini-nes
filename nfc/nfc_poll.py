#!/usr/bin/pyton2.7

from ctypes import *
import time
import signal
import pwd
import grp
import daemon
import lockfile
import logging

logLevel = logging.DEBUG

class App():
    def __init__(self):
        self.libnfc = CDLL("libnfc.so")
        self.libnfcutils = CDLL("libnfcutils.so")

        self.interval = 5 # seconds
        self.uiPollNr = 1 # number of times to poll each interval
        self.uiPeriod = 1 # nfc polling periods each interval

    def run(self):
        logging.debug( "App.run" )
        nfc_open()

        logging.debug( "Entering main loop" )

        while True:
            uid = nfc_poll( uiPollNr, uiPeriod )

            if uid:
                logging.info( "Found NFC tag: {0}".format( uid ) )

            time.sleep( self.interval )

    def cleanup(self):
        logging.debug( "cleanup" )
        nfc_close()


    def nfc_open():
        res = self.libnfcutils.nfcutils_open()

        if res < 0:
            raise OSError( "Error: Unable to open NFC device: {0}".format( res ) )
        else:
            logging.info( "NFC Device Open" )

    def nfc_close():
        res = self.libnfcutils.nfcutils_close()

    def nfc_poll( uiPollNr, uiPeriod ):
        charArray20 = c_char * 20
        uidString = charArray20()

        res = self.libnfcutils.nfcutils_poll( uiPollNr, uiPeriod, uidString )

        if res < 0:
            # On my chipset, it returns a -90 Internal Chip Error when the tag is
            # not present. This sucks as it sounds like a valid error code, but
            # we have to ignore that error as it's a normal condition.
            logging.warning( "Warning: nfc poll: {0}".format( res ) )
            return None
        elif res == 0:
            logging.debug( "No NFC tag found" )
            return None
        elif res == 1:
            logging.debug( "NFC tag found: {0}".format( uidString.value ) )
            return uidString.value


##### Main Startup #####
app = App()
logger = logging.getLogger( "nfc_poll_log" )
logger.setLevel( logLevel )
logFormatter = logging.Formatter( "%(asctime)s - %(name)s - %(levelname)s - %(message)s" )
logHandler = logging.FileHandler( "/var/log/nfc_poll.log" )
logHandler.setFormatter( logFormatter )
logger.addHandler( logHandler )

daemonRunner = daemon.runner.DaemonRunner( app )

with daemonRunner.daemon_context:
    files_preserve = [ logHandler.stream ]
    working_directory = '/var/lib/nfc_poll'
    gid = grp.getgrnam( 'nes' ).gr_gid
    uid = pwd.getpwnam( 'nes' ).pw_uid
    umask = 0o002
    pidfile = lockfile.FileLock( '/var/run/nfc_poll.pid' ),
    signal_map = {
        signal.SIGTERM: app.cleanup,
    }

daemonRunner.do_action()

