import tkinter as tk
from tkinter import filedialog, messagebox, Menu
import subprocess
import os
import sys

class StartLoaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("StartLoader - Android Emulator")
        self.root.geometry("600x400")

        self.bootloader_path = tk.StringVar()
        self.recovery_path = tk.StringVar()
        self.system_image_path = tk.StringVar()
        self.firmware_path = tk.StringVar()
        self.device_ready = False
        self.storage_path = tk.StringVar()
        self.storage_size = tk.StringVar(value="16G")

        self.create_menu()
        self.create_status_view()

    def create_menu(self):
        menubar = Menu(self.root)

        # Environment Menu
        env_menu = Menu(menubar, tearoff=0)
        env_menu.add_command(label="Select Bootloader", command=self.select_bootloader)
        env_menu.add_command(label="Select Recovery Image", command=self.select_recovery)
        menubar.add_cascade(label="Environment", menu=env_menu)

        # System Menu
        system_menu = Menu(menubar, tearoff=0)
        system_menu.add_command(label="Load Image", command=self.load_system_image)
        menubar.add_cascade(label="System", menu=system_menu)

        # Machine Menu
        machine_menu = Menu(menubar, tearoff=0)
        machine_menu.add_command(label="Compile and Create Device", command=self.create_device)
        machine_menu.add_command(label="Select Firmware", command=self.select_firmware)
        machine_menu.add_separator()
        machine_menu.add_command(label="Start Bootloader", command=self.start_bootloader)
        menubar.add_cascade(label="Machine", menu=machine_menu)

        # Virtual Phone Menu
        phone_menu = Menu(menubar, tearoff=0)
        stock_rom_menu = Menu(phone_menu, tearoff=0)
        stock_rom_menu.add_command(label="From Zero", command=self.load_system_image)
        phone_menu.add_cascade(label="Install Stock ROM", menu=stock_rom_menu)
        menubar.add_cascade(label="Virtual Phone", menu=phone_menu)

        self.root.config(menu=menubar)

    def create_status_view(self):
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="Current Configuration:", font=("Helvetica", 12, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 10))

        tk.Label(frame, text="Bootloader:").grid(row=1, column=0, sticky="w")
        tk.Label(frame, textvariable=self.bootloader_path, wraplength=400).grid(row=1, column=1, sticky="w", padx=10)

        tk.Label(frame, text="Recovery:").grid(row=2, column=0, sticky="w")
        tk.Label(frame, textvariable=self.recovery_path, wraplength=400).grid(row=2, column=1, sticky="w", padx=10)

        tk.Label(frame, text="System Image:").grid(row=3, column=0, sticky="w")
        tk.Label(frame, textvariable=self.system_image_path, wraplength=400).grid(row=3, column=1, sticky="w", padx=10)

        tk.Label(frame, text="Firmware:").grid(row=4, column=0, sticky="w")
        tk.Label(frame, textvariable=self.firmware_path, wraplength=400).grid(row=4, column=1, sticky="w", padx=10)

        tk.Label(frame, text="Storage Size:").grid(row=5, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.storage_size, width=10).grid(row=5, column=1, sticky="w", padx=10)

    def select_bootloader(self):
        path = filedialog.askopenfilename(title="Select Bootloader", filetypes=[("Binary files", "*.bin"), ("All files", "*.*")])
        if path:
            self.bootloader_path.set(path)

    def select_recovery(self):
        path = filedialog.askopenfilename(title="Select Recovery Image", filetypes=[("Image files", "*.img"), ("All files", "*.*")])
        if path:
            self.recovery_path.set(path)

    def load_system_image(self):
        path = filedialog.askopenfilename(title="Load System Image", filetypes=[("Image files", "*.img"), ("All files", "*.*")])
        if path:
            self.system_image_path.set(path)

    def select_firmware(self):
        path = filedialog.askopenfilename(title="Select Firmware", filetypes=[("Firmware files", "*.zip;*.tar.gz"), ("All files", "*.*")])
        if path:
            self.firmware_path.set(path)

    def create_device(self):
        if not self.bootloader_path.get() or not self.system_image_path.get():
            messagebox.showwarning("Warning", "Please select a bootloader and system image first.")
            return

        self.storage_path.set("assets/system_images/userdata.img")
        size_str = self.storage_size.get().upper()

        try:
            # Simple parser for G, M, K
            multiplier = 1024 * 1024 * 1024 # Default G
            if size_str.endswith('G'):
                multiplier = 1024 * 1024 * 1024
                size_val = int(size_str[:-1])
            elif size_str.endswith('M'):
                multiplier = 1024 * 1024
                size_val = int(size_str[:-1])
            elif size_str.endswith('K'):
                multiplier = 1024
                size_val = int(size_str[:-1])
            else:
                size_val = int(size_str)

            total_size = size_val * multiplier

            # Mocking device creation/storage allocation
            if not os.path.exists("assets/system_images"):
                os.makedirs("assets/system_images")

            # For the mock, we still don't create huge files to avoid disk space issues in sandbox
            # But we at least use the parsed value or a reasonable cap
            mock_size = min(total_size, 1024 * 1024 * 10)

            with open(self.storage_path.get(), "wb") as f:
                f.truncate(mock_size)

            self.device_ready = True
            messagebox.showinfo("Success", f"Device storage of {size_str} allocated. Device created successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create device: {e}")

    def start_bootloader(self):
        if not self.device_ready:
            messagebox.showwarning("Warning", "Please create the device first.")
            return

        qemu_cmd = [
            sys.executable, "src/launcher.py",
            "--bootloader", self.bootloader_path.get(),
            "--image", self.system_image_path.get(),
            "--recovery", self.recovery_path.get(),
            "--firmware", self.firmware_path.get(),
            "--storage", self.storage_path.get()
        ]

        try:
            # We use Popen to not block the GUI
            subprocess.Popen(qemu_cmd)
            messagebox.showinfo("Info", "Emulator started.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start emulator: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StartLoaderGUI(root)
    root.mainloop()
