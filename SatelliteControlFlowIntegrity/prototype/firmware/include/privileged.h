#ifndef PRIVILEGED_H
#define PRIVILEGED_H
#include <stdint.h>

/* Mission configuration block.
 *
 * The authentication flag lives immediately after the parameter table - the
 * kind of layout that shows up in real flight software, where a configuration
 * struct grows a security field over time. It is exactly what makes the
 * data-only attack (S5) possible. */
struct flight_state {
    uint32_t params[8];
    uint32_t authenticated;
};

extern volatile struct flight_state g_state;

/* Writes a mission parameter. CONTROLLED VULNERABILITY #2: the index is not
 * bounds-checked, so index 8 lands on g_state.authenticated. */
void param_set(uint32_t index, uint32_t value);

/* Gated entry point: checks authentication, then calls the body. */
void priv_raw_write(uint32_t addr, uint32_t value);

/* The body, split out so the auth check is a distinct CFG edge. A direct
 * edge into priv_raw_write_body() is an authentication bypass. */
void priv_raw_write_body(uint32_t addr, uint32_t value);

/* Leftover factory/debug hook, never called in flight. Spawns a task above
 * the ADCS priority - reaching it is a scheduling attack. */
void debug_spawn_rogue_task(void);
#endif
