#ifndef TC_H
#define TC_H
#include <stdint.h>
#include <stddef.h>

/* Telecommand frame (simplified CCSDS-like layout):
 *
 *  +--------+--------+--------+-------------------+
 *  | SYNC   | APID   | LEN    | PAYLOAD (LEN B)   |
 *  | 2 B    | 1 B    | 1 B    | variable          |
 *  +--------+--------+--------+-------------------+
 */
#define TC_SYNC0        0xEBU
#define TC_SYNC1        0x90U
#define TC_HDR_LEN      4U
#define TC_MAX_FRAME    256U

#define APID_ADCS_MODE  0x10U
#define APID_TM_BEACON  0x20U
#define APID_EPS_REPORT 0x30U
#define APID_PLD_CAPT   0x40U
#define APID_PARAM_SET  0x50U
#define APID_PRIV_WRITE 0x60U
#define APID_WD_LOAD    0x70U
#define APID_WD_FIRE    0x71U

void tc_handle_frame(const uint8_t *frame, uint32_t frame_len);
#endif
