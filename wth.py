import ctypes
import sys
import os
from ctypes import wintypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    script = os.path.abspath(sys.argv[0])
    params = ' '.join(sys.argv[1:])
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
    except Exception as e:
        print(f"Failed to elevate: {e}")
        input("Press Enter to exit...")
    sys.exit()
user32 = ctypes.windll.user32
SW_HIDE = 0
SW_SHOW = 5
MOD_ALT = 0x0001
VK_T = 0x54

def total_vanish(show=True):
    targets = ["Shell_TrayWnd", "Shell_SecondaryTrayWnd", "NotifyIconOverflowWindow"]
    cmd = SW_SHOW if show else SW_HIDE
    for class_name in targets:
        hwnd = user32.FindWindowW(class_name, None)
        if hwnd:
            user32.ShowWindow(hwnd, cmd)
            user32.EnableWindow(hwnd, show)

def main():
    if not user32.RegisterHotKey(None, 1, MOD_ALT, VK_T):
        print("!!! ERROR: Alt+T is already taken by another program.")
        print("Try closing other scripts or changing the key.")
        input("Press Enter to exit...")
        return

    print("========================================")
    print("          TASKBAR VANISH MODE           ")
    print("========================================")
    print("HOTKEY: ALT + T")
    print("STATUS: Running...")
    print("\nPress Ctrl+C to quit.")

    is_visible = True
    try:
        msg = wintypes.MSG()
        while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
            if msg.message == 0x0312:  # Hotkey event
                is_visible = not is_visible
                total_vanish(is_visible)
                print(f" >> Taskbar {'VISIBLE' if is_visible else 'VANISHED'}")
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))
    except KeyboardInterrupt:
        print("\nRestoring and exiting...")
    finally:
        total_vanish(True)
        user32.UnregisterHotKey(None, 1)

if __name__ == "__main__":
    main()