import subprocess
import os
import sys

def build_bootloader():
    # Attempt to find the best available toolchain
    toolchains = [
        {"as": "as", "ld": "ld"},
        {"as": "x86_64-w64-mingw32-as", "ld": "x86_64-w64-mingw32-ld"},
        {"as": "i686-w64-mingw32-as", "ld": "i686-w64-mingw32-ld"},
    ]

    selected_tools = None
    for tc in toolchains:
        try:
            subprocess.run([tc["as"], "--version"], capture_output=True)
            selected_tools = tc
            break
        except FileNotFoundError:
            continue

    if not selected_tools:
        print("Error: No suitable assembler ('as' or MinGW) found. Please install the GNU Binutils toolchain.")
        sys.exit(1)

    as_cmd = [selected_tools["as"], "-o", "bootloader/boot.o", "bootloader/boot.S"]
    ld_cmd = [selected_tools["ld"], "--oformat", "binary", "-Ttext", "0x7C00", "-o", "bootloader/boot.bin", "bootloader/boot.o"]

    print("Building bootloader...")

    try:
        print(f"Executing: {' '.join(as_cmd)}")
        subprocess.run(as_cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Assembly failed with exit code {e.returncode}")
        sys.exit(e.returncode)

    try:
        print(f"Executing: {' '.join(ld_cmd)}")
        subprocess.run(ld_cmd, check=True)
        print("Success: bootloader/boot.bin created.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Linking failed with exit code {e.returncode}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    build_bootloader()
