#include "privileged.h"
#include "uart.h"
#include "subsystems.h"
#include "FreeRTOS.h"
#include "task.h"

volatile uint32_t g_tc_authenticated = 0U;

void priv_raw_write_body(uint32_t addr, uint32_t value)
{
    uart_puts("[PRIV] raw write addr="); uart_put_hex(addr);
    uart_puts(" value="); uart_put_hex(value); uart_puts("\r\n");
    uart_puts("*** PRIVILEGED FUNCTION EXECUTED WITHOUT AUTH ***\r\n");
    g_mission_lost = 1U;
}

void priv_raw_write(uint32_t addr, uint32_t value)
{
    if (g_tc_authenticated == 0U) {
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
