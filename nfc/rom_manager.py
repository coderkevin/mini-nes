#!/usr/bin/env python2.7

import psutil
import subprocess

ROMS_PATH = "/home/pi/RetroPie/roms/"
EMULATOR_PATH = "/opt/retropie/supplementary/runcommand/runcommand.sh"
EMULATOR_OPTS = "0 _SYS_"

class RomManager():
    def __init__( self, logger ):
        self.logger = logger

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

    def load( self, romFile ):
        self.logger.info( 'load rom: {}'.format( romFile ) )

        #self.killEmulatorProcs()

        #console = romFile[0:romFile.index('/')]
        #emulatorCmd = "{} {} {} {}".format(
        #    EMULATOR_PATH,
        #    EMULATOR_OPTS,
        #    console,
        #    romFile
        #    )
        #self.logger.info( 'Running emulator command: {}'.format( emulatorCmd ) )


