CROSS_COMPILE ?=
AS = $(CROSS_COMPILE)as
LD = $(CROSS_COMPILE)ld
OBJCOPY = $(CROSS_COMPILE)objcopy
PYTHON = python3

BOOTLOADER_SRC = bootloader/boot.S
BOOTLOADER_OBJ = bootloader/boot.o
BOOTLOADER_BIN = bootloader/boot.bin

.PHONY: all build run clean help

all: build

build: $(BOOTLOADER_BIN)

$(BOOTLOADER_BIN): $(BOOTLOADER_SRC)
	$(AS) -o $(BOOTLOADER_OBJ) $(BOOTLOADER_SRC)
	$(LD) --oformat binary -Ttext 0x7C00 -o $(BOOTLOADER_BIN) $(BOOTLOADER_OBJ)

run: build
	$(PYTHON) src/launcher.py --bootloader $(BOOTLOADER_BIN)

clean:
	rm -f $(BOOTLOADER_OBJ) $(BOOTLOADER_BIN)

help:
	@echo "StartLoader Build System"
	@echo "Targets:"
	@echo "  build   Assemble and link the bootloader"
	@echo "  run     Build and start the emulator"
	@echo "  clean   Remove build artifacts"
	@echo "  help    Show this message"
