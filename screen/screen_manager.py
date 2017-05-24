import os
import shlex
import subprocess
import psutil
import log
import logging
import argparse
import ConfigParser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logLevel = logging.DEBUG;
logFormat = '%(asctime)s - %(levelname)s - %(message)s'
logger = None # This is set to a valid logger in the main, below.

RUNCOMMAND = "/opt/retropie/supplementary/runcommand/runcommand.sh"
EMULATIONSTATION = "/opt/retropie/supplementary/emulationstation/emulationstation.sh"
DEFAULT_ACTION = { 'type': 'dashboard' }

# Action functions

def run_rom( options ):
    if not 'system' in options:
        logger.error( "Expected 'system' option" )
    elif not 'path' in options:
        logger.error( "Expected 'path' option" )
    else:
        system = options[ 'system' ]
        path = options[ 'path' ]

        # Use runcommand to load the rom, then ES after it exits
        logger.info( 'Running rom: {}'.format( path ) )
        cmd = "{} 0 _SYS_ {} '{}'".format( RUNCOMMAND, system, path )
        return cmd

def run_dashboard( options ):
    logger.info( "Running dashboard" )
    return EMULATIONSTATION

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

class ConfigChangeHandler( FileSystemEventHandler ):
    def __init__( self, screen_manager ):
        self.screen_manager = screen_manager
        self.config_file = screen_manager.config_file

    def on_created( self, event ):
        if ( event.src_path == self.config_file ):
            logger.debug( "Config file created: {}".format( event ) )
            self.screen_manager.read_config()

    def on_modified( self, event ):
        if ( event.src_path == self.config_file ):
            logger.debug( "Config file modified: {}".format( event ) )
            self.screen_manager.read_config()

    def on_deleted( self, event ):
        if ( event.src_path == self.config_file ):
            logger.debug( "Config file deleted: {}".format( event ) )
            self.screen_manager.read_config()

class ScreenManager():
    def __init__( self, config_file ):
        self.config_file = config_file
        self.lastAction = None
        self.process = None

        change_handler = ConfigChangeHandler( self )
        self.observer = Observer()
        self.observer.schedule( change_handler, os.path.dirname( config_file ) )

    def read_config( self ):
        action = DEFAULT_ACTION

        config = ConfigParser.RawConfigParser()
        config.read( self.config_file )
        if config.has_section( 'Action' ):
            # Construct a dictionary for the Action section
            action = {}
            for name in config.options( 'Action' ):
                action[ name ] = config.get( 'Action', name )

        if action != self.lastAction:
            self.run_action( action )
        else:
            logger.debug( "Action is same as last action. Ignoring." );

    def run_action( self, action ):
        logger.debug( "Running action: {}".format( action ) )

        self.lastAction = action

        actionFunc = ACTIONS[ action[ 'type' ] ];

        if actionFunc:
            cmd = actionFunc( action )

            if cmd:
                self.run_cmd( cmd )

        else:
            logger.error( "Action '{}' not recognized.".format( action[ 'type' ] ) )

    def run_cmd( self, cmd ):
        if self.process:
            terminate_process( self.process )

        logger.debug( "Running command: {}".format( cmd ) );
        self.process = subprocess.Popen( shlex.split( cmd ) )
        # TODO: Do something if the user exits the process ( like using select+start in RetroArch )

    def start( self ):
        self.read_config()
        self.observer.start()
        self.observer.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser( description="Screen Manager" )
    parser.add_argument( '-c', '--config', default='/dev/shm/screen_manager.cfg' )
    parser.add_argument( '-l', '--log-file', default='/dev/shm/screen_manager.log' )

    args = parser.parse_args()

    logger = log.initLogger( logLevel, logFormat, args.log_file )
    logger.info( "Screen Manager Start" )

    screenManager = ScreenManager( args.config )
    screenManager.start()

