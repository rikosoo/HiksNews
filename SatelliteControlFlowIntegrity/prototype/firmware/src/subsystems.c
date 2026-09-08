#include "subsystems.h"
#include "uart.h"

volatile uint32_t g_mission_lost = 0U;

static uint8_t  s_adcs_mode = 0U;
static uint32_t s_adcs_ticks = 0U;

void adcs_set_mode(uint8_t mode)
{
    s_adcs_mode = mode;
    uart_puts("[ADCS] mode="); uart_put_u32(mode); uart_puts("\r\n");
}

void adcs_step(void)
{
    s_adcs_ticks++;   /* stand-in for the attitude control loop */
}

void tm_send_beacon(void)
{
    uart_puts("[TM  ] beacon ticks="); uart_put_u32(s_adcs_ticks);
    uart_puts(" mode="); uart_put_u32(s_adcs_mode); uart_puts("\r\n");
}

void eps_report(void)
{
    uart_puts("[EPS ] battery nominal\r\n");
}

void payload_capture(void)
{
    uart_puts("[PLD ] capture requested\r\n");
}

void payload_step(void) { }

void eps_kill_switch(void)
{
    g_mission_lost = 1U;
    uart_puts("\r\n*** EPS KILL SWITCH ENGAGED - BUS POWER OFF ***\r\n");
    uart_puts("*** MISSION LOST ***\r\n");
}

void payload_wipe(void)
{
    g_mission_lost = 1U;
    uart_puts("\r\n*** PAYLOAD MEMORY WIPED ***\r\n");
}
