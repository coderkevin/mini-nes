#!/usr/bin/env python2.7

import traceback
import argparse
import signal
import grp
import daemon
from daemon import pidfile
import log
import logging
import nfc_poll

debug_p = True

def start_daemon( pidf, logf ):
    # This launches the daemon in its context

    global debug_p

    if debug_p:
        print( "nfc_poll_daemon: entered start_daemon()")
        print( "nfc_poll_daemon: pidf={}  logf={}".format( pidf, logf ) )

    try:
        with daemon.DaemonContext(
            working_directory='/var/lib/nfc_poll',
            gid = grp.getgrnam( 'pi' ).gr_gid,
            umask=0o002,
            pidfile=pidfile.TimeoutPIDLockFile( pidf ),
            ) as context:

            logLevel = logging.INFO
            logFormat = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

            logger = log.initLogger( logLevel, logFormat, logf )
            logger.info( "nfc_poll_daemon: entered daemon context" )

            try:
                options = nfc_poll.initConfig( logger )
                logger.info( "nfc_poll_daemon: options: {}".format( options ) )

                app = nfc_poll.NFCPoll( options, logger )
                context.signal_map = {
                    signal.SIGTERM: app.cleanup
                    }
                logger.info( "nfc_poll_daemon: running app" )
                app.run()
            except:
                logger.error( traceback.format_exc() )
                sys.exit(1)

    except:
        print( "Unhandled Exception: {}".format( traceback.format_exc() ) )
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser( description="NFC Poll Daemon" )
    parser.add_argument( '-p', '--pid-file', default='/var/run/nfc_poll.pid' )
    parser.add_argument( '-l', '--log-file', default='/dev/shm/nfc_poll.log' )

    args = parser.parse_args()

    start_daemon( args.pid_file, args.log_file )

