#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <nfc/nfc.h>
#include <nfc/nfc-types.h>

#include "nfcutils.h"

// Error codes
#define ERR_INIT      -101
#define ERR_OPEN      -102
#define ERR_INITIATOR -103
#define ERR_POLL      -104

static void print_usage( const char *progname )
{
	printf( "usage: %s [-v]\n", progname );
	printf( "  -v\t verbose display\n" );
}

int main( int argc, const char *argv[] )
{
	bool verbose = false;
	int uiPollNr = 20;
	int uiPeriod = 2;

	// Display libnfc version
	const char *libnfcVersion = nfc_version();

	if ( verbose ) {
		printf( "%s uses libnfc %s\n", argv[0], libnfcVersion );
	}

	if ( argc != 1 ) {
		if ( ( argc = 2 ) && ( 0 == strcmp( "-v", argv[1] ) ) ) {
			verbose = true;
		} else {
			print_usage( argv[0] );
			exit( EXIT_FAILURE );
		}
	}

	char uid[20];
	int res = 0;

	if ( ( res = nfcutils_open() ) < 0 ) {
		fprintf( stderr, "NFC init/open failed: %d\n", res );
		exit( EXIT_FAILURE );
	}

	if ( verbose ) {
		printf( "NFC device opened\n" );
	}

	if ( ( res = nfcutils_poll( uiPollNr, uiPeriod, uid ) ) < 0 ) {
		fprintf( stderr, "NFC poll failed: %d\n", res );
	} else if ( res > 0 ) {
		printf( "UID: %s\n", uid );
	} else {
		printf( "No NFC tag found" );
	}

	nfcutils_close();

	if ( verbose ) {
		printf( "NFC device closed\n" );
	}
	exit( EXIT_SUCCESS );
}

