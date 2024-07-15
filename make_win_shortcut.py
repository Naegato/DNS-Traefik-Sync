import os
import winshell
from win32com.client import Dispatch

def create_shortcut(bat_file_path):
    desktop = winshell.start_menu()  # Get the Start Menu folder path
    shortcut_path = os.path.join(desktop, "Programs", "dns-sync.lnk")
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = bat_file_path
    shortcut.WorkingDirectory = os.path.dirname(bat_file_path)
    shortcut.IconLocation = bat_file_path
    shortcut.save()
    print(f"Shortcut created at {shortcut_path}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bat_file_path = os.path.join(script_dir, 'cmd.bat')

    if os.path.exists(bat_file_path):
        create_shortcut(bat_file_path)
    else:
        print(f"{bat_file_path} does not exist. Please run makecmd.py first.")

if __name__ == "__main__":
    main()