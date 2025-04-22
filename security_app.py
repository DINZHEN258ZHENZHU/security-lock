import tkinter as tk
from tkinter import messagebox, ttk
import os
import sys
import winreg
import hashlib
import logging
import ctypes
import subprocess

# Configure logging
logging.basicConfig(
    filename="security_app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class SecurityApp:
    def __init__(self):
        """Initialize MPU Security Lock Screen application to prevent unauthorized access."""
        self.window = tk.Tk()
        self.window.title("MPU Security Lock Screen")
        
        # Fullscreen mode and always on top
        self.window.attributes('-fullscreen', True)
        self.window.attributes('-topmost', True)
        self.window.protocol("WM_DELETE_WINDOW", self.disable_event)
        self.window.bind("<Alt-F4>", self.disable_event)
        self.window.bind("<Escape>", self.disable_event)  # Block ESC key

        # Security configuration
        self.countdown = 120  # Countdown in seconds
        self.max_attempts = 3  # Maximum password attempts
        self.attempts = 0
        self.lock_file = os.path.join(os.environ.get("TEMP", "/tmp"), "mpu_security.lock")
        
        # Initialize password manager (default password: 123456)
        self.pwd_manager = PasswordManager()
        
        # Check if another instance is running
        if self.check_already_running():
            logging.info("Another instance is running, exiting.")
            sys.exit(0)
            
        # Enable autostart
        self.enable_autostart()
        
        # Create UI with darker colors
        self.create_ui()
        
        # Start countdown
        self.update_timer()
        
        self.window.mainloop()

    def create_ui(self):
        """Create improved UI with better visibility."""
        # Main frame with dark background
        main_frame = tk.Frame(self.window, bg="#0D1B2A")
        main_frame.pack(fill="both", expand=True)

        # Center container
        center_frame = tk.Frame(main_frame, bg="#0D1B2A")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title with better contrast
        tk.Label(
            center_frame,
            text="MPU SECURITY LOCK",
            font=("Arial", 28, "bold"),
            fg="#E0E1DD",  # Lighter color for better visibility
            bg="#0D1B2A",
            pady=20
        ).pack()

        # Countdown label
        self.time_label = tk.Label(
            center_frame,
            text=f"Time remaining: {self.countdown} seconds",
            font=("Arial", 18),
            fg="#FF3333",  # Brighter red
            bg="#0D1B2A",
            pady=10
        )
        self.time_label.pack()

        # Password input frame
        pwd_frame = tk.Frame(center_frame, bg="#0D1B2A")
        pwd_frame.pack(pady=20)

        tk.Label(
            pwd_frame,
            text="Enter Password:",
            font=("Arial", 14),
            fg="#E0E1DD",  # Lighter color
            bg="#0D1B2A"
        ).pack(side="left", padx=10)

        self.pwd_entry = ttk.Entry(
            pwd_frame,
            show="*",
            font=("Arial", 14),
            width=20
        )
        self.pwd_entry.pack(side="left", padx=10)
        self.pwd_entry.focus_set()

        # Custom ttk style
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=10)
        style.configure("TEntry", padding=5)
        style.map("TButton",
                background=[('active', '#415A77'), ('!active', '#1B263B')],
                foreground=[('active', '#FFFFFF'), ('!active', '#FFFFFF')])

        # Submit button
        self.submit_btn = ttk.Button(
            center_frame,
            text="SUBMIT",
            command=self.check_password,
            style="TButton"
        )
        self.submit_btn.pack(pady=20)

        # Error label
        self.error_label = tk.Label(
            center_frame,
            text="",
            font=("Arial", 12),
            fg="#FF3333",
            bg="#0D1B2A",
            pady=5
        )
        self.error_label.pack()

        # Admin contact info
        tk.Label(
            center_frame,
            text="Contact Admin: security@mpu.edu.mo | Emergency: +853 12345678",
            font=("Arial", 10, "italic"),
            fg="#778DA9",  # Better contrast
            bg="#0D1B2A",
            pady=10
        ).pack()

    def update_timer(self):
        """Update countdown timer."""
        if self.countdown > 0:
            self.time_label.config(text=f"Time remaining: {self.countdown} seconds")
            self.countdown -= 1
            self.window.after(1000, self.update_timer)
        else:
            logging.warning("Countdown expired, triggering lock.")
            self.trigger_lock()

    def check_password(self):
        """Verify entered password."""
        input_pwd = self.pwd_entry.get()
        
        if self.pwd_manager.verify(input_pwd):
            logging.info("Password verified successfully.")
            messagebox.showinfo("Success", "Password correct, system unlocked.")
            self.cleanup()
            self.window.destroy()
        else:
            self.attempts += 1
            remaining = self.max_attempts - self.attempts
            logging.warning(f"Wrong password, attempts remaining: {remaining}")
            if remaining > 0:
                self.error_label.config(text=f"Wrong password! Attempts left: {remaining}")
                self.pwd_entry.delete(0, tk.END)
            else:
                logging.error("Maximum attempts exceeded, triggering lock.")
                self.trigger_lock()

    def trigger_lock(self):
        """Trigger system lock with optional disk formatting."""
        messagebox.showerror(
            "SECURITY LOCK",
            "Too many failed attempts or timeout!\nSystem has been locked.\nContact administrator."
        )
        
        logging.error("System locked due to security policy.")
        
        # Lock workstation (Windows only)
        if sys.platform == "win32":
            try:
                ctypes.windll.user32.LockWorkStation()
                logging.info("Workstation locked successfully.")
            except Exception as e:
                logging.error(f"Failed to lock workstation: {e}")
        
        # Optional disk formatting - WARNING: DESTRUCTIVE OPERATION
        # Uncomment below code ONLY if you want to enable disk formatting
        # IMPORTANT: This will ERASE ALL DATA on specified drives!
        """
        try:
            logging.warning("Initiating disk formatting...")
            # List of drives to format (modify as needed)
            drives_to_format = ['D:', 'E:']  # Avoid C: to prevent system damage
            
            for drive in drives_to_format:
                try:
                    # Format command (Windows)
                    subprocess.run(
                        ['format', drive, '/FS:NTFS', '/Q', '/Y'],
                        check=True,
                        shell=True
                    )
                    logging.error(f"Drive {drive} formatted successfully.")
                except Exception as e:
                    logging.error(f"Failed to format {drive}: {e}")
        except Exception as e:
            logging.error(f"Disk formatting failed: {e}")
        """
        
        # Create lock file
        try:
            with open(self.lock_file, "w") as f:
                f.write("LOCKED")
            logging.info("Lock file created successfully.")
        except Exception as e:
            logging.error(f"Failed to create lock file: {e}")

        self.window.destroy()

    def cleanup(self):
        """Clean up lock file."""
        if os.path.exists(self.lock_file):
            try:
                os.remove(self.lock_file)
                logging.info("Lock file removed.")
            except Exception as e:
                logging.error(f"Failed to remove lock file: {e}")

    def check_already_running(self):
        """Check if another instance is running."""
        return os.path.exists(self.lock_file)

    def enable_autostart(self):
        """Enable autostart on boot (Windows only)."""
        if sys.platform != "win32":
            logging.warning("Non-Windows system, skipping autostart.")
            return
        
        try:
            exe_path = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
            key = winreg.HKEY_CURRENT_USER
            reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            reg_key = winreg.OpenKey(key, reg_path, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(reg_key, "MPUSecurity", 0, winreg.REG_SZ, exe_path)
            winreg.CloseKey(reg_key)
            logging.info("Autostart enabled successfully.")
        except Exception as e:
            logging.error(f"Failed to enable autostart: {e}")

    def disable_event(self, event=None):
        """Prevent window close events."""
        return "break"

class PasswordManager:
    """Password manager using salted password hashing."""
    def __init__(self):
        self.salt = b'mpu_comp2116_salt'
        self.stored_hash = self._hash_password("123456")  # Default password
        
    def _hash_password(self, password):
        """Generate salted password hash."""
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            self.salt,
            100000
        )
        
    def verify(self, input_pwd):
        """Verify input password."""
        input_hash = self._hash_password(input_pwd)
        return input_hash == self.stored_hash

if __name__ == "__main__":
    try:
        app = SecurityApp()
    except PermissionError:
        logging.error("Insufficient permissions, requires admin rights.")
        messagebox.showerror("Permission Error", "Please run as administrator.")