#!/usr/bin/env python2.7

import sys
import psutil
import subprocess
import log
import logging

ROMS_PATH = "/home/pi/RetroPie/roms/"
EMULATOR_PATH = "/opt/retropie/supplementary/runcommand/runcommand.sh"
EMULATOR_OPTS = "0 _SYS_"

class RomManager():
    def __init__( self, logger ):
        self.logger = logger
        self.rom = None

    def killProcs( self, procNames ):
        for proc in psutil.process_iter():
            if proc.name() in procNames:
                pid = str( proc.as_dict(attrs=['pid'])['pid'] )
                name = proc.as_dict(attrs=['name'])['name']
                signal = "-9" if name.startswith( "kodi" ) else "-15"
                self.logger.debug( "killing {} (pid: {})".format( name, pid ) )
                subprocess.call( [ "sudo", "kill", signal, pid ] )

    def killEmulatorProcs( self ):
        procNames = [
            "retroarch", "ags", "uae4all2", "uae4arm", "capricerpi", "linapple", "hatari", "stella",
            "atari800", "xroar", "vice", "daphne", "reicast", "pifba", "osmose", "gpsp", "jzintv",
            "basiliskll", "mame", "advmame", "dgen", "openmsx", "mupen64plus", "gngeo", "dosbox", "ppsspp",
            "simcoupe", "scummvm", "snes9x", "pisnes", "frotz", "fbzx", "fuse", "gemrb", "cgenesis", "zdoom",
            "eduke32", "lincity", "love", "alephone", "micropolis", "openbor", "openttd", "opentyrian",
            "cannonball", "tyrquake", "ioquake3", "residualvm", "xrick", "sdlpop", "uqm", "stratagus",
            "wolf4sdl", "solarus", "emulationstation", "emulationstatio", "kodi", "kodi.bin"
        ]
        self.killProcs( procNames )

    def clear( self ):
        if self.rom:
            self.logger.info( "Clearing rom for default operation" )
            self.rom = None
            self.killEmulatorProcs()
            emulatorCmd = "{} {} none none".format( EMULATOR_PATH, EMULATOR_OPTS )
            subprocess.call( "sudo openvt -c 1 -s -f {} &".format( emulatorCmd ), shell=True );

    def load( self, rom ):
        if rom != self.rom:
            self.logger.info( 'Loading rom: {}'.format( rom ) )
            self.rom = rom
            self.killEmulatorProcs()

            console = rom[0:rom.index('/')]
            emulatorCmd = "{} {} {} {}{}".format(
                EMULATOR_PATH,
                EMULATOR_OPTS,
                console,
                ROMS_PATH,
                rom
                )
            self.logger.info( 'Running emulator command: {}'.format( emulatorCmd ) )
            subprocess.call( "sudo openvt -c 1 -s -f {} &".format( emulatorCmd ), shell=True );

if __name__ == "__main__":
    logLevel = logging.DEBUG
    logFormat = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    logger = log.initLogger( logLevel, logFormat )

    try:
        app = RomManager( logger )
        app.load( sys.argv[1] )
    except:
        logger.error( traceback.format_exc() )
        sys.exit(1)


