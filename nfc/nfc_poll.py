from ctypes import *
from time import sleep

debug = True

libnfc = CDLL("libnfc.so")
libnfcutils = CDLL("libnfcutils.so")

def nfc_open():
    res = libnfcutils.nfcutils_open()

    if res < 0:
        raise OSError( "Error: Unable to open NFC device: {0}".format( res ) )
    else:
        if debug:
            print "NFC Device Open"


def nfc_close():
    res = libnfcutils.nfcutils_close()

def nfc_poll( uiPollNr, uiPeriod ):
    charArray20 = c_char * 20
    uidString = charArray20()

    res = libnfcutils.nfcutils_poll( uiPollNr, uiPeriod, uidString )

    if res < 0:
        # On my chipset, it returns a -90 Internal Chip Error when the tag is
        # not present. This sucks as it sounds like a valid error code, but
        # we have to ignore that error as it's a normal condition.
        if debug:
            print( "Warning: nfc poll: {0}".format( res ) )
        return None
    elif res == 0:
        print "No NFC tag found"
        return None
    elif res == 1:
        print "NFC tag found: {0}".format( uidString.value )
        return uidString.value

def nfc_poll_continuous( interval, callback ):

    # TODO: Set shutdown criteria, maybe catch SIGINT and return?
    while True:
        uid = nfc_poll( 1, 1 )

        if uid:
            if debug:
                print "Found NFC tag: {0}".format( uid )
            callback( uid )

        sleep( interval )

