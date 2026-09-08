#include "uart.h"

#define UART0_BASE  0x40004000UL
#define UART_DATA   (*(volatile uint32_t *)(UART0_BASE + 0x00))
#define UART_STATE  (*(volatile uint32_t *)(UART0_BASE + 0x04))
#define UART_CTRL   (*(volatile uint32_t *)(UART0_BASE + 0x08))

#define STATE_TX_FULL  (1U << 0)
#define STATE_RX_FULL  (1U << 1)

void uart_init(void)
{
    UART_CTRL = 0x3U;   /* TX + RX enable */
}

void uart_putc(char c)
{
    while (UART_STATE & STATE_TX_FULL) { }
    UART_DATA = (uint32_t) c;
}

void uart_puts(const char *s)
{
    while (*s) { uart_putc(*s++); }
}

void uart_put_hex(uint32_t v)
{
    static const char digits[] = "0123456789abcdef";
    uart_puts("0x");
    for (int i = 28; i >= 0; i -= 4) {
        uart_putc(digits[(v >> i) & 0xFU]);
    }
}

void uart_put_u32(uint32_t v)
{
    char buf[11];
    int i = 10;
    buf[i] = '\0';
    if (v == 0U) { uart_putc('0'); return; }
    while (v > 0U && i > 0) { buf[--i] = (char)('0' + (v % 10U)); v /= 10U; }
    uart_puts(&buf[i]);
}

int uart_getc_nonblock(void)
{
    if (UART_STATE & STATE_RX_FULL) {
        return (int)(UART_DATA & 0xFFU);
    }
    return -1;
}
