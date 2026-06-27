import argparse
import subprocess
import sys
import os

def main():
    parser = argparse.ArgumentParser(description="StartLoader Android Emulator Launcher")
    parser.add_argument("--image", help="Path to the Android system image")
    parser.add_argument("--bootloader", default="bootloader/boot.bin", help="Path to the custom bootloader binary")
    parser.add_argument("--dry-run", action="store_true", help="Display the QEMU command without executing it")
    parser.add_argument("--memory", default="2G", help="Amount of memory for the emulator (default: 2G)")

    args = parser.parse_args()

    qemu_cmd = [
        "qemu-system-x86_64",
        "-m", args.memory,
        "-drive", f"file={args.bootloader},format=raw,index=0,media=disk",
    ]

    if args.image:
        if not os.path.exists(args.image):
            print(f"Error: Image file {args.image} not found.")
            sys.exit(1)
        qemu_cmd.extend(["-drive", f"file={args.image},format=raw,index=1,media=disk"])

    print("Executing command:")
    print(" ".join(qemu_cmd))

    if args.dry_run:
        print("\nDry run completed.")
        return

    try:
        subprocess.run(qemu_cmd, check=True)
    except FileNotFoundError:
        print("\nError: qemu-system-x86_64 not found. Please install QEMU.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"\nQEMU exited with error: {e}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
