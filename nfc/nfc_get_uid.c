#include <err.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>

#include <nfc/nfc.h>
#include <nfc/nfc-types.h>

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

	printf( "%s uses libnfc %s\n", argv[0], libnfcVersion );
	if ( argc != 1 ) {
		if ( ( argc = 2 ) && ( 0 == strcmp( "-v", argv[1] ) ) ) {
			verbose = true;
		} else {
			print_usage( argv[0] );
			exit( EXIT_FAILURE );
		}
	}
}

