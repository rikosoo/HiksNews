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
};
