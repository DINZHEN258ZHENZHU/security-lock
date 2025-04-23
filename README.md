# MPU Security Lock Screen

## Overview

Picture this: you're happily coding away, sipping your third coffee of the night, when—*poof!*—you dramatically keel over from a caffeine overdose (or, you know, just peacefully ascend to the great server in the sky). Your family, bless their curious hearts, rushes to your computer, eager to uncover the mysteries of your digital life. But fear not! The **MPU Security Lock Screen** is here to save your secrets! This Python-powered fortress locks your PC tighter than a vault, ensuring your *questionable browser history* and *top-secret meme collection* remain safe from prying eyes. With a sleek `tkinter` interface, a countdown timer, and a password that laughs in the face of nosy relatives, this app is your posthumous privacy pal. Oh, and it has an optional (but *very* disabled) disk-wiping feature for when you *really* want to take your secrets to the grave—use it at your own peril!

**WARNING**: The commented-out disk formatting feature will **OBLITERATE ALL DATA** on specified drives if enabled. It’s like throwing your hard drive into a volcano. Do **NOT** enable unless you’re 100% sure, and even then, maybe don’t. We’re not responsible for turning your PC into a very expensive paperweight.

---

Watch this viedio : https://youtu.be/fae5vs6ps2U


## Development Process
**Methodology**: Agile development with 2-week sprints  
**Rationale**:
- Optimal for 3-person team collaboration
- Enables rapid iteration based on testing feedback
- Supports parallel module development

### Core Features

- **Fullscreen Lock Screen**: A bulletproof GUI that takes over your screen, blocking `Alt+F4`, `Escape`, and window close attempts like a digital bouncer.
- **Password Verification**: Uses salted SHA-256 hashing (`hashlib.pbkdf2_hmac`) to protect your secrets with a password (default: `123456`—because who needs creativity when you’re already gone?).
- **Countdown Timer**: Gives intruders 120 seconds to crack the code before the system locks them out.
- **Limited Attempts**: Three strikes, and you’re out! After three wrong passwords, the system locks faster than you can say “oops.”
- **System Lock**: On Windows, locks the workstation using `ctypes.windll.user32.LockWorkStation`. Non-Windows users get a polite warning instead.
- **Autostart on Boot**: Sneakily starts the app every time your PC boots (Windows only, via registry magic).
- **Single Instance Check**: Uses a lock file to ensure only one instance runs, because even digital ghosts don’t need duplicates.
- **Logging**: Keeps a detailed diary of all actions and errors in `security_app.log` for posthumous debugging.

### User Interface

- **Sleek Dark Theme**: A moody dark blue (#0D1B2A) background with high-contrast text that screams “stay away” in style.
- **Dynamic Feedback**: Error messages pop up on-screen (e.g., “Wrong password! Attempts left: X”), and the countdown timer glows menacingly in red.
- **Responsive Design**: Centers perfectly on any screen, from your grandma’s ancient monitor to your 4K gaming rig.
- **Instant Input**: The password field is ready for action the moment the app launches.
- **Fancy Button**: The “SUBMIT” button changes colors when hovered, because even security apps deserve a little flair.

### Optional (Commented-Out) Feature

- **Disk Formatting (HERE BE DRAGONS)**: A disabled code block in `trigger_lock` can format drives (e.g., `D:`, `E:`) using the Windows `format` command.
  - **WARNING**: Enabling this will **WIPE ALL DATA** on the targeted drives. It’s the digital equivalent of setting your computer on fire.
  - **DISCLAIMER**: If you enable this and lose your cat videos, tax records, or that novel you’ve been writing for a decade, don’t haunt us. Back up your data and test in a safe environment first.

---

## Requirements

- **Operating System**: Windows 7 or later (full functionality). Non-Windows systems (Linux, macOS) support the lock screen but skip workstation locking and autostart.
- **Python**: Version 3.6 or higher (for running the script directly).
- **Dependencies**: None! Uses only Python standard libraries (`tkinter`, `winreg`, `hashlib`, `logging`, `ctypes`, `subprocess`).
- **Administrator Privileges**: Needed for workstation locking and autostart setup.

---

## Installation

### Running the Python Script

1. Ensure Python 3.6+ is installed (check with `python --version`).

2. Save `security_app.py` to a directory (e.g., `C:\SecurityApp`).

3. Open a command prompt and navigate to the directory:

   ```bash
   cd C:\SecurityApp
   ```

4. Run the script:

   ```bash
   python security_app.py
   ```

5. Run as administrator (right-click `cmd` &gt; "Run as administrator") for full features like locking and autostart.

### Creating a Standalone Executable

To share the app without needing Python installed:

1. Install PyInstaller:

   ```bash
   pip install pyinstaller
   ```

2. Navigate to the directory with `security_app.py`:

   ```bash
   cd C:\SecurityApp
   ```

3. Create a single executable:

   ```bash
   pyinstaller --onefile --windowed security_app.py
   ```

   - `--onefile`: Packs everything into one `.exe`.
   - `--windowed`: Hides the console for a cleaner GUI experience.
   - Optional: Add a custom icon with `--icon=app.ico` (provide an `.ico` file).

4. Find the executable in `dist/security_app.exe`.

5. Copy the `.exe` to any Windows PC and run it (admin rights needed for full functionality).

---

## Usage

1. **Launch the App**:

   - Run `security_app.py` or `security_app.exe`.
   - The lock screen engulfs your screen, ready to defend your digital dignity.

2. **Enter Password**:

   - Default password: `123456`.
   - Type it, hit “SUBMIT” or press Enter.
   - Correct password? You’re in, and the app vanishes.
   - Wrong password? You get 3 tries before the system says “nope” and locks.

3. **Countdown Timer**:

   - You’ve got 120 seconds to prove you’re not an impostor.
   - Timer runs out? System locks, and your secrets stay safe.

4. **System Lock**:

   - After 3 failed attempts or timeout, the system locks (Windows workstation lock).
   - A lock file (`mpu_security.lock`) is created in `%TEMP%` to keep things secure.

5. **Contact Admin**:

   - Locked out? The UI suggests emailing `security@mpu.edu.mo` or calling `+853 12345678`.
   - (Pro tip: If you’re the admin, maybe leave a note with the password somewhere safe.)

6. **Unlocking**:

   - An admin must unlock the workstation and delete `%TEMP%\mpu_security.lock`.

---

## Security Notes

- **Default Password**: Hardcoded as `123456` (hashed, don’t worry). Change it in `PasswordManager.__init__` for real-world use.
- **Lock File**: Prevents multiple instances but can be manually deleted. Secure your `%TEMP%` directory if needed.
- **Admin Privileges**: Locking and autostart need admin rights. Run as administrator to avoid hiccups.
- **Disk Formatting (Disabled)**: Left commented out to save your data. Don’t enable unless you’re ready to say goodbye to your drives.

**DISCLAIMER**: This app is your digital bouncer, but use it wisely. We’re not responsible for locked-out families, lost data, or existential crises caused by enabling disk formatting.

---

## Configuration

### Changing the Default Password

1. Open `security_app.py`.

2. In `PasswordManager.__init__`, update:

   ```python
   self.stored_hash = self._hash_password("123456")  # Default password
   ```

3. Replace `"123456"` with your new password.

4. Save and re-run or re-package.

### Adjusting the Countdown Timer

1. In `SecurityApp.__init__`, change:

   ```python
   self.countdown = 120  # Countdown in seconds
   ```

2. Set your preferred duration.

### Enabling Disk Formatting (Seriously, Don’t)

1. In `SecurityApp.trigger_lock`, uncomment the formatting code:

   ```python
   try:
       logging.warning("Initiating disk formatting...")
       drives_to_format = ['D:', 'E:']  # Avoid C: to prevent system damage
       ...
   ```

2. Update `drives_to_format` with target drives.

3. **WARNING**: Test in a virtual machine first. This will erase everything on the listed drives.

**DISCLAIMER**: Enabling this is like inviting a wrecking ball to your hard drive. Back up everything and proceed with caution. We can’t stress this enough.

---

## Troubleshooting

- **App Won’t Start**:

  - Check Python 3.6+ installation (for script).
  - Run as administrator for locking/autostart.
  - Review `security_app.log` for clues.

- **UI Problems**:

  - Ensure `tkinter` works (`python -m tkinter`).
  - Test on various screen resolutions.

- **Executable Fails**:

  - Verify Microsoft Visual C++ Redistributable is installed.
  - Exclude the `.exe` from antivirus scans.
  - Rebuild with PyInstaller if issues persist.

- **Locking Fails**:

  - Run as administrator.
  - Confirm Windows OS (non-Windows lacks `LockWorkStation`).

- **Formatting Errors** (if enabled):

  - Ensure drives exist and are accessible.
  - Run as admin for `format` command.
  - Check `security_app.log` for details.

---

## Building and Packaging

To create a standalone `.exe`:

1. Install PyInstaller:

   ```bash
   pip install pyinstaller
   ```

2. Package the app:

   ```bash
   pyinstaller --onefile --windowed security_app.py
   ```

3. Optional: Add an icon or clean up:

   ```bash
   pyinstaller --onefile --windowed --icon=app.ico --clean security_app.py
   ```

4. Find `dist/security_app.exe`, ready for any Windows PC.

**Note**: The `.exe` bundles all dependencies, so no Python needed on the target machine.

---

## License


Provided as-is, no warranty. Use at your own risk. The developers are not liable for data loss, system damage, or family feuds over locked computers, especially if you enable disk formatting.

---

![image](https://github.com/user-attachments/assets/be02faf8-9e07-49f1-81d9-c4096849631d)

![image](https://github.com/user-attachments/assets/d6bdfb92-095e-40c6-928b-e970a912fab1)

