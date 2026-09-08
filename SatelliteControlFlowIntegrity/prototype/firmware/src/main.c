/* CubeSat-like flight software: five FreeRTOS tasks on an ARM Cortex-M3. */
#include "FreeRTOS.h"
#include "task.h"

#include "uart.h"
#include "tc.h"
#include "subsystems.h"

/* ---- tc_rx: receives telecommands from the ground station over UART ---- */
static void task_tc_rx(void *pv)
{
    static uint8_t frame[TC_MAX_FRAME];
    uint32_t idx = 0U, need = TC_HDR_LEN;
    (void)pv;

    for (;;) {
        int c = uart_getc_nonblock();
        if (c < 0) { vTaskDelay(pdMS_TO_TICKS(2)); continue; }

        frame[idx++] = (uint8_t)c;

        if (idx == TC_HDR_LEN) {
            need = TC_HDR_LEN + (uint32_t)frame[3];
            if (need > TC_MAX_FRAME) { need = TC_MAX_FRAME; }
        }
        if (idx >= need) {
            tc_handle_frame(frame, idx);
            idx = 0U;
            need = TC_HDR_LEN;
        }
    }
}

/* ---- adcs: attitude control loop, the hard real-time consumer ---- */
static void task_adcs(void *pv)
{
    TickType_t last = xTaskGetTickCount();
    (void)pv;
    for (;;) {
        adcs_step();
        vTaskDelayUntil(&last, pdMS_TO_TICKS(10));
    }
}

static void task_eps(void *pv)
{
    (void)pv;
    for (;;) { vTaskDelay(pdMS_TO_TICKS(5000)); }
}

static void task_tm_tx(void *pv)
{
    (void)pv;
    for (;;) {
        tm_send_beacon();
        vTaskDelay(pdMS_TO_TICKS(2000));
    }
}

static void task_payload(void *pv)
{
    (void)pv;
    for (;;) { payload_step(); vTaskDelay(pdMS_TO_TICKS(50)); }
}

int main(void)
{
    uart_init();
    uart_puts("\r\n=== CubeSat flight software boot ===\r\n");

    xTaskCreate(task_tc_rx,   "tc_rx",   256, NULL, 4, NULL);
    xTaskCreate(task_adcs,    "adcs",    192, NULL, 3, NULL);
    xTaskCreate(task_eps,     "eps",     160, NULL, 2, NULL);
    xTaskCreate(task_tm_tx,   "tm_tx",   192, NULL, 1, NULL);
    xTaskCreate(task_payload, "payload", 160, NULL, 1, NULL);

    vTaskStartScheduler();
    for (;;) { }
}

void vApplicationMallocFailedHook(void) { for (;;) { } }

void HardFault_Handler(void)
{
    uart_puts("\r\n*** HARD FAULT ***\r\n");
    for (;;) { }
}
