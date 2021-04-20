
# Dual Boot Bluetooth Pair

This is a tool I use to pair a bluetooth device with my Windows OS and Manjaro OS on my dual boot laptop.

## Disclaimer

> This script involves accessing and modifying system files on the Windows / Linux systems and may risk damaging your computer. Proceed with the below steps at your own risk.

## Instructions

> I recommend backing up all config files before attempting the below steps.

The scripts in this project are intended to be executed on your Linux OS using [Python3](https://www.python.org/).

 1. Boot into Linux and pair bluetooth device(s). You'll need the newly generated `info` and `attributes` files in `/var/lib/bluetooth/<ADAPTOR_MAC_ADDRESS>/<DEVICE_MAC_ADDRESS>/`.
 2. Reboot into Windows and pair bluetooth device(s).
 3. Download [PSExec](http://live.sysinternals.com/psexec.exe) and run the following command from a Command Prompt running in Administator mode:

```
PsExec64.exe -s -i regedit /e C:\BTKeys.reg HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services\BTHPORT\Parameters\Keys
```

 4. Copy the `C:\BTKeys.reg` file to a USB key (or leave on `C:` drive if it's accessible from the Linux OS).
 5. Turn off bluetooth device(s) and boot back into Linux. Don't pair the device again in Linux. It might generate a new mac address, which will break the Windows pairing. (I don't know if this is normal, but it's what happens with my Logitech G604).
 6. Copy the `BTKeys.reg` file to your Linux filesystem.
 7. Run `clean_reg_file.py --file_path BTKeys.reg --output clean.reg` to clean the file (converts encoding to UTF8 and strips quotation marks).
 8. Run `bluetooth_fix.py --reg_path clean.reg`.
 9. From a terminal with `sudo`, navigate to `/var/lib/bluetooth/<ADAPTOR_MAC_ADDRESS>/`.
 10. Make a new directory corresponding to the device mac address from `BTKeys.reg`.
 11. Copy `info` and `attributes` from the old mac address directory to the new one.
 12. Open `/var/lib/bluetooth/<ADAPTOR_MAC>/<NEW_DEVICE_MAC>/info` and modify the values as per output from step 8.
 13. Restart bluetooth with `sudo systemctl restart bluetooth`.

