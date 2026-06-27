# StartLoader: Android Software Image Emulator

This project provides an Android software image emulator powered by a custom bootloader image. It uses QEMU to emulate an x86_64 system and boots a custom bootloader that can then load an Android system image.

## Project Structure

- `bootloader/`: Contains the custom bootloader source code (`boot.S`) and build artifacts.
- `src/`: Contains the emulator launcher script (`launcher.py`).
- `include/`: Header files for the bootloader and other components.
- `scripts/`: Helper scripts for development and testing.
- `Makefile`: Build system for the project.

## Requirements

- `gcc` / `as` / `ld`: GNU Toolchain for assembling and linking the bootloader.
- `python3`: For running the emulator launcher.
- `qemu-system-x86_64`: The QEMU emulator (must be installed on the host system).

## Getting Started

### 1. Build the Bootloader

To assemble and link the custom bootloader:

```bash
make build
```

This will generate `bootloader/boot.bin`.

### 2. Run the Emulator

To start the emulator using the default settings:

```bash
make run
```

Or run the launcher script directly for more options:

```bash
python3 src/launcher.py --image /path/to/android.img --memory 4G
```

### 3. Dry Run

To see the QEMU command that will be executed without actually starting the emulator:

```bash
python3 src/launcher.py --dry-run
```

## Custom Bootloader

The bootloader is written in x86 assembly (`bootloader/boot.S`). It is a minimal real-mode bootloader that prints a message to the screen. In a real-world scenario, this bootloader would be responsible for initializing hardware, setting up the CPU state, and loading the Android kernel from the system image.

## License

This project is licensed under the MIT License.
