#ifndef UART_H
#define UART_H
#include <stdint.h>
#include <stddef.h>

/* CMSDK APB UART0 on the MPS2-AN385 - the "radio link" to the ground station. */
void uart_init(void);
void uart_putc(char c);
void uart_puts(const char *s);
void uart_put_hex(uint32_t v);
void uart_put_u32(uint32_t v);
int  uart_getc_nonblock(void);   /* -1 when no byte is pending */
#endif
