# Flight software for QEMU mps2-an385 (ARM Cortex-M3)
CROSS   ?= arm-none-eabi-
CC      := $(CROSS)gcc
OBJCOPY := $(CROSS)objcopy
SIZE    := $(CROSS)size

KERNEL  := third_party/FreeRTOS-Kernel
PORT    := $(KERNEL)/portable/GCC/ARM_CM3
MEMMANG := $(KERNEL)/portable/MemMang

BUILD   := build
TARGET  := $(BUILD)/flight.elf

SRCS := \
  src/startup.c src/main.c src/libc_stubs.c src/uart.c src/tc.c src/subsystems.c src/privileged.c \
  $(KERNEL)/tasks.c $(KERNEL)/queue.c $(KERNEL)/list.c $(KERNEL)/timers.c \
  $(PORT)/port.c $(MEMMANG)/heap_4.c

INCS := -Iinclude -I$(KERNEL)/include -I$(PORT)

# -O0 and no stack protector: the injected vulnerability must stay reachable
# and the stack layout must stay predictable for the attack scripts.
CFLAGS := -mcpu=cortex-m3 -mthumb -O0 -g3 -ffreestanding -fno-stack-protector \
          -fno-builtin -Wall -Wextra -Wno-unused-parameter $(INCS)
LDFLAGS := -mcpu=cortex-m3 -mthumb -T mps2_an385.ld -nostartfiles -nostdlib \
           -Wl,-Map=$(BUILD)/flight.map

all: $(TARGET)

$(TARGET): $(SRCS) mps2_an385.ld | $(BUILD)
	$(CC) $(CFLAGS) $(SRCS) $(LDFLAGS) -o $@
	$(SIZE) $@

$(BUILD):
	mkdir -p $(BUILD)

run: $(TARGET)
	qemu-system-arm -M mps2-an385 -cpu cortex-m3 -m 16m -nographic \
	  -kernel $(TARGET) -serial mon:stdio

clean:
	rm -rf $(BUILD)

.PHONY: all run clean
