import subprocess
import time 
import pyautogui
import pygetwindow as gw
import os 

def open_app(app_name: str) -> bool:
    """
     Launch an application by name (Windows: uses the Start menu's app resolution).
    Returns True if the launch command was issued without error, False otherwise.
    """
    try:
        os.startfile(app_name)
        return focus_window(app_name)
    except Exception:
        return False

def click(x: int, y: int) -> None:
    screen_w, screen_h = pyautogui.size()
    if not (0 <= x < screen_w and 0 <= y < screen_h):
        return f"ERROR: coordinates ({x}, {y}) are outside screen bounds ({screen_w}x{screen_h})"
    pyautogui.click(x, y)
    return "clicked"
def double_click(x: int, y: int) -> str:
    screen_w, screen_h = pyautogui.size()
    if not(0 <= x < screen_w and 0 <= y < screen_h):
        return f"ERROR: coordinates ({x}, {y}) are outside screen bounds ({screen_w}x{screen_h})"
    pyautogui.doubleClick(x,y)
    return "Double-clicked"
def type_text(text: str, interval: float = 0.02) -> None:
    pyautogui.write(text, interval=interval)

def press_key(key: str) -> None:
    pyautogui.press(key)

def scroll(amount: int) -> None:
    """Positive scrolls up, negative scrolls down."""
    pyautogui.scroll(amount)

def take_screenshot(path: str = "screenshot.png")-> str:
    """Saves a screenshot and returns the file path"""
    screenshot = pyautogui.screenshot()
    screenshot.save(path)
    return path

def focus_window(name_substr: str, timeout: float = 6.0)->bool:
    """
    Poll for a window whose title contains name_substr (case-insensitive)
    and bring it to the foreground. Returns True if found and focused,
    False if it never appeared within the timeout.
    """
    end_time = time.time() + timeout
    while time.time() < end_time:
        for title in gw.getAllTitles():
            if title.strip() and name_substr.lower() in title.lower():
                try:
                    win = gw.getWindowsWithTitle(title)[0]
                    win.activate()
                    win.maximize() 
                    return True
                except Exception:
                    pass
        time.sleep(0.3)
    return False        

