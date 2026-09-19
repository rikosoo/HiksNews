#ifndef WATCHDOG_H
#define WATCHDOG_H
#include <stdint.h>

#define WD_IRQ_NUM 30U        /* external interrupt line, vector index 16+30 */

void wd_init(void);
void wd_load(uint32_t off, const uint8_t *data, uint32_t len);
void wd_fire(uint32_t len);
void sec_irq_handler(void);
#endif
