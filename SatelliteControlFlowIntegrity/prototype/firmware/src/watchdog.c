#include "watchdog.h"
#include "uart.h"

/* Safety-monitor interrupt.
 *
 * The flight software raises a dedicated low-priority interrupt to process a
 * watchdog message uplinked from the ground. The handler therefore runs in
 * exception context, directly off the vector table.
 */
#define NVIC_ISER0  (*(volatile uint32_t *)0xE000E100UL)
#define NVIC_ISPR0  (*(volatile uint32_t *)0xE000E200UL)
#define NVIC_IPR_B  ((volatile uint8_t *)0xE000E400UL)

volatile uint32_t g_wd_len = 0U;
volatile uint8_t  g_wd_buf[192];

static void wd_copy(uint8_t *dst, const volatile uint8_t *src, uint32_t n)
{
    for (uint32_t i = 0U; i < n; i++) { dst[i] = src[i]; }
}

/* CONTROLLED VULNERABILITY #3
 *
 * The armed length is trusted and copied into a 16-byte buffer on the handler
 * stack. Unlike the other injected flaws, this one overflows *inside exception
 * context*. The handler is invoked straight from the vector table, so its own
 * frame is the only thing between the buffer and the EXC_RETURN value that the
 * epilogue pops into the PC:
 *
 *     offset  0..15   local[16]
 *     offset 16       saved r7
 *     offset 20       saved LR = EXC_RETURN
 *
 * Forging that slot hijacks the exception return itself - a transfer that no
 * control-flow graph contains, because no CFG contains any exception return.
 */
void sec_irq_handler(void)
{
    uint8_t local[16];

    if (g_wd_len == 0U) { return; }
    wd_copy(local, g_wd_buf, g_wd_len);
    g_wd_len = 0U;
    (void)local;
}

void wd_init(void)
{
    NVIC_IPR_B[WD_IRQ_NUM] = 0xE0U;          /* lowest priority */
    NVIC_ISER0 = (1UL << WD_IRQ_NUM);
}

void wd_load(uint32_t off, const uint8_t *data, uint32_t len)
{
    if (off >= sizeof(g_wd_buf)) { return; }
    if (off + len > sizeof(g_wd_buf)) { len = sizeof(g_wd_buf) - off; }
    for (uint32_t i = 0U; i < len; i++) { g_wd_buf[off + i] = data[i]; }
    uart_puts("[WD  ] segment loaded at "); uart_put_u32(off); uart_puts("\r\n");
}

void wd_fire(uint32_t len)
{
    if (len > sizeof(g_wd_buf)) { len = sizeof(g_wd_buf); }
    g_wd_len = len;
    uart_puts("[WD  ] watchdog message armed, len="); uart_put_u32(len);
    uart_puts("\r\n");
    NVIC_ISPR0 = (1UL << WD_IRQ_NUM);        /* raise the safety-monitor IRQ */
}
