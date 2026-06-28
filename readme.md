# StartLoader: Android Software Image Emulator

This project provides an Android software image emulator powered by a custom bootloader image. It is designed for both Windows and Linux environments.

## Project Structure

- `bootloader/`: Contains the custom bootloader source code (`boot.S`) and build artifacts.
- `src/`: Contains the emulator launcher script (`launcher.py`), GUI (`gui.py`), and extras.
- `assets/`: Directory for storing bootloaders, recoveries, system images, and firmwares.
- `include/`: Header files for the bootloader and other components.
- `scripts/`: Helper scripts for setup, development, and updates (`setup.py`, `update.py`, `build.py`).
- `Makefile`: Build system for the project.

## Requirements

- `gcc` / `as` / `ld`: GNU Toolchain or MinGW (for Windows) for assembling and linking the bootloader.
- `python3`: For running the emulator launcher.
- `tkinter`: Python's GUI toolkit.
- `qemu-system-x86_64`: The QEMU emulator (must be installed on the host system).

## Getting Started

### 1. Build the Bootloader

To assemble and link the custom bootloader:

```bash
make build
```

**Cross-compiling (e.g. using MinGW):**

```bash
make build CROSS_COMPILE=x86_64-w64-mingw32-
```

Or if you don't have `make` installed:

```bash
# On Linux
python3 scripts/build.py

# On Windows
build.bat
```

The `build.py` script will automatically attempt to find `as`/`ld` or their MinGW equivalents.

This will generate `bootloader/boot.bin`.

### 2. Run the Emulator

You can run the emulator via the GUI or the command line.

#### Using the GUI (Recommended)

To start the graphical user interface:

```bash
python3 src/launcher.py --gui
```

**GUI Workflow:**
1. **Environment** -> **Select Bootloader**: Choose your bootloader binary (e.g., Moto or Google bootloader).
2. **Environment** -> **Select Recovery Image**: Choose a compatible recovery image.
3. **System** -> **Load Image**: Select the Android system image.
4. **Machine** -> **Compile and Create Device**: Allocate storage (total storage size can be specified) and prepare the virtual device.
5. **Machine** -> **Select Firmware**: Load additional core device files (Moto firmwares contain core device files).
6. **Machine** -> **Start Bootloader**: Launch the emulator.

**Deploying a Stock ROM (Alternative Path):**
1. **Virtual Phone** -> **Install Stock ROM** -> **From Zero**: Select the stock ROM or GSI system image.
2. Follow the rest of the **Machine** menu steps to start the emulator.

**Booting from Tarballs:**
1. **Boot** -> **boot by blxxx.tar.md5**: Directly boot using components from a Samsung-style bootloader tarball.

**Extras:**
1. **Extras** -> **Custom ROM Creator**: Tool for creating personalized Android system images.

#### Using the Command Line

To start the emulator with default settings:

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

## Dependency Management

StartLoader can automatically check for and install missing dependencies (like QEMU) on Linux systems. This is triggered automatically when you run the launcher, or can be manually invoked:

```bash
python3 scripts/setup.py
```

In the GUI, you can also use **Setup** -> **Install Dependencies**.

## Updating

To update StartLoader to the latest version:

```bash
python3 scripts/update.py
```

## License

This project is licensed under the MIT License.
