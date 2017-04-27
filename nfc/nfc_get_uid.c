#include <err.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>

#include <nfc/nfc.h>
#include <nfc/nfc-types.h>

#include "utils/nfc-utils.h"

// Error codes
#define ERR_INIT      -101
#define ERR_OPEN      -102
#define ERR_INITIATOR -103
#define ERR_POLL      -104

// Modulations to scan for
const nfc_modulation nmModulations[1] = {
	{ .nmt = NMT_ISO14443A, .nbr = NBR_106 },
};
const size_t szModulations = 1;

const uiPollNr = 20;
const uiPeriod = 2;

static nfc_device *pnd = NULL;
static nfc_context *context;

static void stop_polling( int sig )
{
	(void) sig;

	if ( pnd != NULL ) {
		nfc_abort_command( pnd );
	} else {
		nfc_exit( context );
		exit( EXIT_FAILURE );
	}
}

static int open() {
	signal( SIGINT, stop_polling );

	nfc_init( &context );
	if ( NULL == context ) {
		return ERR_INIT;
	}

	pnd = nfc_open( context, NULL );

	if ( NULL == pnd ) {
		nfc_exit( context );
		return ERR_OPEN;
	}

	if ( nfc_initiator_init( pnd ) < 0 ) {
		return ERR_INITIATOR;
		nfc_close( pnd );
		nfc_exit( context );
		exit( EXIT_FAILURE );
	}
}

static void close() {

	nfc_close( pnd );
	nfc_exit( context );
}

static int poll( int uiPollNr, int uiPeriod, char *uid) {
	int res = 0;
	nfc_target nt;

	if ( ( res = nfc_initiator_poll_target( pnd, nmModulations, szModulations, uiPollNr, uiPeriod, &nt ) ) < 0 ) {
		return ERR_POLL;
	}

	if ( res > 0 ) {
		nfc_iso14443a_info *pnai = &nt.nti.nai;
		int i;
		int charIndex = 0;

		// Print the hex numbers to the uid string.
		for ( i = 0; i < pnai->szUidLen; i++ ) {
			sprintf( uid + charIndex, "%02x", pnai->abtUid[ i ] );
			charIndex += 2;
		}

		return 1;
	} else {
		return 0;
	}
}

static void print_usage( const char *progname )
{
	printf( "usage: %s [-v]\n", progname );
	printf( "  -v\t verbose display\n" );
}

int main( int argc, const char *argv[] )
{
	bool verbose = false;

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

	if ( ( res = open() ) < 0 ) {
		fprintf( stderr, "NFC init/open failed: %d\n", res );
		exit( EXIT_FAILURE );
	}

	if ( verbose ) {
		printf( "NFC reader: %s opened\n", nfc_device_get_name( pnd ) );
	}

	if ( ( res = poll( uiPollNr, uiPeriod, uid ) ) < 0 ) {
		fprintf( stderr, "NFC poll failed: %d\n", res );
	} else if ( res > 0 ) {
		printf( "UID: %s\n", uid );
	} else {
		printf( "No NFC tag found" );
	}

	close();

	if ( verbose ) {
		printf( "NFC reader: %s closed\n", nfc_device_get_name( pnd ) );
	}
	exit( EXIT_SUCCESS );
}

