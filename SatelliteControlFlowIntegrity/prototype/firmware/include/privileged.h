#ifndef PRIVILEGED_H
#define PRIVILEGED_H
#include <stdint.h>

/* Authentication state for privileged telecommands. Set only by a successful
 * key exchange, which the prototype never performs: it is always 0. */
extern volatile uint32_t g_tc_authenticated;

/* Gated entry point: checks authentication, then calls the body. */
void priv_raw_write(uint32_t addr, uint32_t value);

/* The body, split out so the auth check is a distinct CFG edge. A direct
 * edge into priv_raw_write_body() is an authentication bypass. */
void priv_raw_write_body(uint32_t addr, uint32_t value);

/* Leftover factory/debug hook, never called in flight. Spawns a task above
 * the ADCS priority - reaching it is a scheduling attack. */
void debug_spawn_rogue_task(void);
#endif
