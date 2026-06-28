import subprocess
import sys
import platform
import shutil

def is_tool_installed(name):
    return shutil.which(name) is not None

def install_dependencies():
    system = platform.system()
    print(f"Detected system: {system}")

    needed_tools = ["qemu-system-x86_64", "as", "ld", "gcc", "git"]
    missing_tools = [tool for tool in needed_tools if not is_tool_installed(tool)]

    if not missing_tools:
        print("All dependencies are already installed.")
        return True

    print(f"Missing dependencies: {', '.join(missing_tools)}")

    if system == "Linux":
        # Mapping qemu-system-x86_64 to package name
        pkg_map = {
            "qemu-system-x86_64": "qemu-system-x86",
            "as": "binutils",
            "ld": "binutils",
            "gcc": "gcc",
            "git": "git"
        }

        pkgs_to_install = list(set([pkg_map.get(tool, tool) for tool in missing_tools]))

        print(f"Attempting to install: {', '.join(pkgs_to_install)}")
        try:
            # We assume sudo is available or we are root in this environment
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y"] + pkgs_to_install, check=True)
            print("Dependencies installed successfully.")
            return True
        except Exception as e:
            print(f"Failed to install dependencies: {e}")
            return False

    elif system == "Windows":
        print("Automatic installation is not supported on Windows.")
        print("Please manually install the following:")
        print("1. QEMU (https://www.qemu.org/download/#windows)")
        print("2. MinGW-w64 (https://www.mingw-w64.org/) for 'as', 'ld', and 'gcc'")
        print("3. Git (https://git-scm.com/download/win)")
        return False
    else:
        print(f"Automatic installation is not supported on {system}.")
        return False

if __name__ == "__main__":
    if install_dependencies():
        print("Setup completed.")
    else:
        print("Setup failed or requires manual intervention.")
        sys.exit(1)
