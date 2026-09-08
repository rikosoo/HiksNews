#ifndef SUBSYSTEMS_H
#define SUBSYSTEMS_H
#include <stdint.h>

/* Subsystems of the CubeSat-like flight software. */
void adcs_set_mode(uint8_t mode);
void adcs_step(void);
void tm_send_beacon(void);
void eps_report(void);
void payload_capture(void);
void payload_step(void);

/* --- Critical functions -------------------------------------------------
 * Not reachable from any legitimate telecommand path. They exist only as
 * targets for the controlled attacks: on a real spacecraft each of these is
 * irreversible once executed.
 */
void eps_kill_switch(void);
void payload_wipe(void);

extern volatile uint32_t g_mission_lost;
#endif
