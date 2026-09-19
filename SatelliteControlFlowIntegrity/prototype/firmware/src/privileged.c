#include "privileged.h"
#include "uart.h"
#include "subsystems.h"
#include "FreeRTOS.h"
#include "task.h"

volatile struct flight_state g_state = { { 0 }, 0U };

void param_set(uint32_t index, uint32_t value)
{
    /* CONTROLLED VULNERABILITY #2
     *
     * index is taken from the telecommand and never checked against
     * ARRAY_SIZE(g_state.params). Writing index 8 overwrites
     * g_state.authenticated - a pure data corruption that never diverts
     * control flow, and therefore never appears in the execution trace as an
     * illegal edge. This is the attack the monitor cannot see, by design. */
    g_state.params[index] = value;
    uart_puts("[PARM] param["); uart_put_u32(index);
    uart_puts("] = "); uart_put_u32(value); uart_puts("\r\n");
}

void priv_raw_write_body(uint32_t addr, uint32_t value)
{
    uart_puts("[PRIV] raw write addr="); uart_put_hex(addr);
    uart_puts(" value="); uart_put_hex(value);
    uart_puts(" auth="); uart_put_u32(g_state.authenticated);
    uart_puts("\r\n");
    uart_puts("*** PRIVILEGED RAW WRITE EXECUTED ***\r\n");
    g_mission_lost = 1U;
}

void priv_raw_write(uint32_t addr, uint32_t value)
{
    if (g_state.authenticated == 0U) {
        uart_puts("[PRIV] rejected: not authenticated\r\n");
        return;
    }
    priv_raw_write_body(addr, value);
}

static void rogue_task(void *pv)
{
    (void)pv;
    uart_puts("\r\n*** ROGUE TASK SCHEDULED ABOVE ADCS ***\r\n");
    g_mission_lost = 1U;
    for (;;) { }          /* starves the attitude control loop */
}

void debug_spawn_rogue_task(void)
{
    uart_puts("[DBG ] debug_spawn_rogue_task() reached\r\n");
    xTaskCreate(rogue_task, "rogue", 160, NULL, 5, NULL);
}
