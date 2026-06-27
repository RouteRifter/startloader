import subprocess
import os
import sys

def build_bootloader():
    as_cmd = ["as", "-o", "bootloader/boot.o", "bootloader/boot.S"]
    ld_cmd = ["ld", "--oformat", "binary", "-Ttext", "0x7C00", "-o", "bootloader/boot.bin", "bootloader/boot.o"]

    print("Building bootloader...")

    try:
        print(f"Executing: {' '.join(as_cmd)}")
        subprocess.run(as_cmd, check=True)
    except FileNotFoundError:
        print("Error: 'as' (GNU Assembler) not found. Please install the GNU Binutils or GCC toolchain.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error: Assembly failed with exit code {e.returncode}")
        sys.exit(e.returncode)

    try:
        print(f"Executing: {' '.join(ld_cmd)}")
        subprocess.run(ld_cmd, check=True)
        print("Success: bootloader/boot.bin created.")
    except FileNotFoundError:
        print("Error: 'ld' (GNU Linker) not found. Please install the GNU Binutils or GCC toolchain.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error: Linking failed with exit code {e.returncode}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    build_bootloader()
