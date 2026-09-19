/* Minimal startup for Cortex-M3 / MPS2-AN385. */
#include <stdint.h>

extern uint32_t _etext, _sdata, _edata, _sbss, _ebss, _estack;
extern int main(void);

void vPortSVCHandler(void);
void xPortPendSVHandler(void);
void xPortSysTickHandler(void);

static void default_handler(void) { for (;;) { } }

void Reset_Handler(void)
{
    uint32_t *src = &_etext;
    for (uint32_t *dst = &_sdata; dst < &_edata; ) { *dst++ = *src++; }
    for (uint32_t *dst = &_sbss; dst < &_ebss; ) { *dst++ = 0U; }
    main();
    for (;;) { }
}

void HardFault_Handler(void);
void sec_irq_handler(void);

__attribute__((section(".isr_vector"), used))
void (* const g_vectors[])(void) = {
    (void (*)(void)) &_estack,
    Reset_Handler,
    default_handler,        /* NMI          */
    HardFault_Handler,      /* HardFault    */
    default_handler,        /* MemManage    */
    default_handler,        /* BusFault     */
    default_handler,        /* UsageFault   */
    0, 0, 0, 0,
    vPortSVCHandler,        /* SVCall       */
    default_handler,        /* DebugMon     */
    0,
    xPortPendSVHandler,     /* PendSV       */
    xPortSysTickHandler,    /* SysTick      */

    /* External interrupts. The safety-monitor line is the only one used. */
    default_handler, default_handler, default_handler, default_handler,  /*  0-3  */
    default_handler, default_handler, default_handler, default_handler,  /*  4-7  */
    default_handler, default_handler, default_handler, default_handler,  /*  8-11 */
    default_handler, default_handler, default_handler, default_handler,  /* 12-15 */
    default_handler, default_handler, default_handler, default_handler,  /* 16-19 */
    default_handler, default_handler, default_handler, default_handler,  /* 20-23 */
    default_handler, default_handler, default_handler, default_handler,  /* 24-27 */
    default_handler, default_handler,                                    /* 28-29 */
    sec_irq_handler,                                                     /* 30    */
    default_handler,                                                     /* 31    */
};
