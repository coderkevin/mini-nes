import sys
import logging

def initLogger( logLevel, logFormat, logFile = None ):
    logger = logging.getLogger( 'NFCPoll' )
    logger.setLevel( logLevel )

    logHandler = None

    if logFile:
        logHandler = logging.FileHandler( logFile )
    else:
        logHandler = logging.StreamHandler( sys.stdout )

    logHandler.setLevel( logLevel )
    logHandler.setFormatter( logging.Formatter( logFormat ) )
    logger.addHandler( logHandler )

    return logger

