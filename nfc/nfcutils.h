#ifndef NFCUTILS_H
#define NFCUTILS_H

/**
 * Open an NFC device.
 *
 * @return int 0 on success, negative on error.
 */
int nfcutils_open();

/**
 * Close the currently opened NFC device.
 */
void nfcutils_close();

/**
 * Poll the currently opened NFC device for tags nearby.
 *
 * @param [in] int uiPollNr The number of times to poll before giving up.
 * @param [in] int uiPeriod The periods to try for each time.
 * @param [out] char[20] uid The buffer in which to write the resulting UID as a string.
 * @return int 1 if tag found, 0 if no tag found, negative on error.
 */
int nfcutils_poll( int uiPollNr, int uiPeriod, char *uid);

#endif
