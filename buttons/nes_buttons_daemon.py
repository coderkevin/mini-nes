#!/usr/bin/env python2.7

import traceback
import argparse
import signal
import grp
import daemon
from daemon import pidfile
import log
import logging
import nes_buttons

debug_p = True

def start_daemon( pidf, logf ):
    # This launches the daemon in its context

    global debug_p

    if debug_p:
        print( "nes_buttons_daemon: entered start_daemon()" )
        print( "nes_buttons_daemon: pidf={} logf={}".format( pidf, logf ) )

    try:
        with daemon.DaemonContext(
            working_directory='/var/lib/nes_buttons',
            gid = grp.getgrnam( 'nes' ).gr_gid,
            umask=0o002,
            pidfile=pidfile.TimeoutPIDLockFile( pidf ),
            ) as context:

            logLevel = logging.INFO
            logFormat = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

            logger = log.initLogger( logLevel, logFormat, logf )
            logger.info( "nes_buttons_daemon: entered daemon context" )

            try:
                app = nes_buttons.NESButtons( logger )
                logger.info( "nes_buttons_daemon: running app" )
                app.run()
            except:
                logger.error( traceback.format_exc() )
                sys.exit(1)

    except:
        print( "Unhandled exception: {}".format( traceback.format_exc() ) )
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser( description="NES Buttons Daemon" )
    parser.add_argument( '-p', '--pid-file', default='/var/run/nes_buttons.pid' )
    parser.add_argument( '-l', '--log-file', default='/var/run/nes_buttons.log' )

    args = parser.parse_args()

    start_daemon( args.pid_file, args.log_file )

