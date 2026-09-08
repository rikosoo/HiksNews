#include "tc.h"
#include "uart.h"
#include "subsystems.h"

/* ------------------------------------------------------------------------
 * Telecommand dispatch table. Legitimate control flow only ever reaches the
 * four handlers below; nothing here can reach eps_kill_switch() or
 * payload_wipe(). Any observed edge into those functions is, by construction,
 * a control-flow violation.
 * ---------------------------------------------------------------------- */

typedef void (*tc_handler_t)(const uint8_t *arg, uint32_t arg_len);

static void h_adcs_mode(const uint8_t *arg, uint32_t arg_len)
{
    adcs_set_mode(arg_len > 0U ? arg[0] : 0U);
}

static void h_tm_beacon(const uint8_t *arg, uint32_t arg_len)
{
    (void)arg; (void)arg_len;
    tm_send_beacon();
}

static void h_eps_report(const uint8_t *arg, uint32_t arg_len)
{
    (void)arg; (void)arg_len;
    eps_report();
}

static void h_pld_capture(const uint8_t *arg, uint32_t arg_len)
{
    (void)arg; (void)arg_len;
    payload_capture();
}

static void h_unknown(const uint8_t *arg, uint32_t arg_len)
{
    (void)arg; (void)arg_len;
    uart_puts("[TC  ] rejected: unknown APID\r\n");
}

static tc_handler_t lookup_handler(uint8_t apid)
{
    switch (apid) {
        case APID_ADCS_MODE:  return h_adcs_mode;
        case APID_TM_BEACON:  return h_tm_beacon;
        case APID_EPS_REPORT: return h_eps_report;
        case APID_PLD_CAPT:   return h_pld_capture;
        default:              return h_unknown;
    }
}

static void tc_copy(uint8_t *dst, const uint8_t *src, uint32_t n)
{
    for (uint32_t i = 0U; i < n; i++) { dst[i] = src[i]; }
}

/* ------------------------------------------------------------------------
 * CONTROLLED VULNERABILITY
 *
 * The declared LEN field is trusted and used as the copy length into a
 * fixed 64-byte stack buffer. The handler pointer sits immediately after the
 * buffer, and the saved return address sits after the frame record, so a
 * single overflow reaches both:
 *
 *   ctx.buf[64] | ctx.handler | ... | saved r7 | saved LR
 *        ^ATK-1/3 write through here      ^ATK-2      ^ATK-1/3 target
 * ---------------------------------------------------------------------- */
void tc_handle_frame(const uint8_t *frame, uint32_t frame_len)
{
    struct {
        uint8_t      buf[64];
        tc_handler_t handler;
    } ctx;

    if (frame_len < TC_HDR_LEN) { return; }
    if (frame[0] != TC_SYNC0 || frame[1] != TC_SYNC1) {
        uart_puts("[TC  ] rejected: bad sync\r\n");
        return;
    }

    uint8_t  apid = frame[2];
    uint32_t len  = frame[3];

    ctx.handler = lookup_handler(apid);

    /* VULNERABILITY: len is attacker-controlled and never checked against
     * sizeof(ctx.buf). This is the single injected flaw of the prototype. */
    tc_copy(ctx.buf, &frame[TC_HDR_LEN], len);

    ctx.handler(ctx.buf, len);
}
