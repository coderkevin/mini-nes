import os
import shlex
import subprocess
import psutil
import log
import logging
import argparse
import ConfigParser

logLevel = logging.DEBUG;
logFormat = '%(asctime)s - %(levelname)s - %(message)s'
logger = None # This is set to a valid logger in the main, below.

RUNCOMMAND = "/opt/retropie/supplementary/runcommand/runcommand.sh"
EMULATIONSTATION = "/opt/retropie/supplementary/emulationstation/emulationstation.sh"
DEFAULT_ACTION = { 'type': 'dashboard' }

# Action functions

def run_rom( options ):
    system = options[ 'system' ]
    path = options[ 'path' ]

    logger.info( 'Running rom: {}'.format( path ) )
    cmd = "{} 0 _SYS_ {} '{}'".format( runcommand, system, path )
    return subprocess.Popen( shlex.split( cmd ) )

def run_dashboard( options ):
    logger.info( "Running dashboard" )
    return subprocess.Popen( EMULATIONSTATION )

ACTIONS = {
    'dashboard': run_dashboard,   # Expects no options
    'rom': run_rom,               # Expects { system, path }
}

def terminate_process( process ):
    logger.info( "Terminating current process" )
    children = psutil.Process( process.pid ).children( recursive=True )
    for child in children:
        child.terminate()
    process.terminate()

class ScreenManager():
    def __init__( self, configFile ):
        self.configFile = configFile
        self.lastAction = None

    def read_config_action( self, configFile ):
        config = ConfigParser.RawConfigParser()
        config.read( configFile )

        if config.has_section( 'Action' ):
            return config.options( 'Action' )
        else:
            return DEFAULT_ACTION

    def run_action( self, action ):
        logger.debug( "Running action: {}".format( action ) )
        self.lastAction = action

        actionFunc = ACTIONS[ action[ 'type' ] ];

        if actionFunc:
            actionFunc( action )
        else:
            logger.error( "Action '{}' not recognized.".format( action[ 'type' ] ) )

    def start( self ):
        action = self.read_config_action( self.configFile )
        self.run_action( action )

if __name__ == "__main__":
    parser = argparse.ArgumentParser( description="Screen Manager" )
    parser.add_argument( '-c', '--config', default='/dev/shm/screen_manager.cfg' )
    parser.add_argument( '-l', '--log-file', default='/dev/shm/screen_manager.log' )

    args = parser.parse_args()

    logger = log.initLogger( logLevel, logFormat, args.log_file )

    screenManager = ScreenManager( args.config )
    screenManager.start()

