#!/usr/bin/env python2.7

import argparse
import signal
import grp
import daemon
from daemon import pidfile
from nfc_poll import NFCPoll

debug_p = True

def start_daemon( pidf, logf ):
    # This launches the daemon in its context

    global debug_p

    if debug_p:
        print( "nfc_poll_daemon: entered start_daemon()")
        print( "nfc_poll_daemon: pidf={}  logf={}".format( pidf, logf ) )

    with daemon.DaemonContext(
        working_directory='/var/lib/nfc_poll',
        gid = grp.getgrnam( 'nes' ).gr_gid,
        umask=0o002,
        pidfile=pidfile.TimeoutPIDLockFile( pidf ),
        ) as context:

        app = NFCPoll( logf )
        context.signal_map = {
            signal.SIGTERM: app.cleanup
            }
        app.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser( description="NFC Poll Daemon" )
    parser.add_argument( '-p', '--pid-file', default='/var/run/nfc_poll.pid' )
    parser.add_argument( '-l', '--log-file', default='/var/log/nfc_poll.log' )

    args = parser.parse_args()

    start_daemon( args.pid_file, args.log_file )

