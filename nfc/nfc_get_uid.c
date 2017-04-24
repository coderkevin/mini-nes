#include <err.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>

#include <nfc/nfc.h>
#include <nfc/nfc-types.h>

#include "utils/nfc-utils.h"

// Modulations to scan for
const nfc_modulation nmModulations[2] = {
	{ .nmt = NMT_ISO14443A, .nbr = NBR_106 },
	{ .nmt = NMT_ISO14443B, .nbr = NBR_106 },
};
const size_t szModulations = 5;

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

static void print_usage( const char *progname )
{
	printf( "usage: %s [-v]\n", progname );
	printf( "  -v\t verbose display\n" );
}

int main( int argc, const char *argv[] )
{
	bool verbose = false;

	signal( SIGINT, stop_polling );

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

	nfc_target nt;
	int res = 0;

	nfc_init( &context );
	if ( NULL == context ) {
		ERR( "Unable to init libnfc (malloc)" );
		exit( EXIT_FAILURE );
	}

	pnd = nfc_open( context, NULL );

	if ( NULL == pnd ) {
		ERR( "%s", "Unable to open NFC device." );
		nfc_exit( context );
		exit( EXIT_FAILURE );
	}

	if ( nfc_initiator_init( pnd ) < 0 ) {
		nfc_perror( pnd, "nfc_initiator_init" );
		nfc_close( pnd );
		nfc_exit( context );
		exit( EXIT_FAILURE );
	}

	if ( verbose ) {
		printf( "NFC reader: %s opened\n", nfc_device_get_name( pnd ) );
	}

	nfc_close( pnd );
	nfc_exit( context );

	if ( verbose ) {
		printf( "NFC reader: %s closed\n", nfc_device_get_name( pnd ) );
	}
	exit( EXIT_SUCCESS );
}

