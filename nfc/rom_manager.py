#!/usr/bin/env python2.7

import sys
import os
import grp
import pwd
import psutil
import subprocess
import log
import logging

ROMS_PATH = "/home/pi/RetroPie/roms/"
EMULATOR_PATH = "/opt/retropie/supplementary/runcommand/runcommand.sh"
DASHBOARD_PATH = "/opt/retropie/supplementary/emulationstation/emulationstation.sh"
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
            emulatorCmd = DASHBOARD_PATH
            subprocess.call( "sudo -u pi bash {} &".format( emulatorCmd ), shell=True );

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
            self.logger.debug( 'Running emulator command: {}'.format( emulatorCmd ) )

            subprocess.call( "bash {} &".format( emulatorCmd ), shell=True, preexec_fn=demote( 'pi', 'pi' ) );

def demote( user, group ):
    def set_ids():
        os.setgid( grp.getgrnam( group ).gr_gid )
        os.setuid( pwd.getpwnam( user ).pw_uid )

    return set_ids

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


