from pywinauto import Desktop
import time

def list_ui_elements(window_title_substr: str, timeout: float = 6.0) -> list[dict]:
    """
    Return clickable UI elements (name, type, center coordinates) for the
    first window whose title contains window_title_substr.
    """
    end_time = time.time()+timeout
    while time.time()< end_time:
        try:
            win = Desktop(backend="uia").window(title_re=f".*{window_title_substr}.*")
            elements = []
            for ctrl in win.descendants():
                try:
                    rect = ctrl.rectangle()
                    name = ctrl.window_text()
                    if not name.strip():
                        continue  # skip unlabeled elements, mostly noise
                    elements.append({
                        "name": name,
                        "control_type": ctrl.friendly_class_name(),
                        "x": (rect.left + rect.right) // 2,
                        "y": (rect.top + rect.bottom) // 2,
                    })
                except Exception:
                    continue
            if elements:
                return elements    
        except Exception:
            pass # some elements throw on inspection; skip rather than crash the whole scan
        time.sleep(0.3)
    return []
# NOTE: UIA-based element lookup is reliable for native Windows apps (tested: Notepad).
# Electron/Chromium apps (tested: Spotify) often expose only a minimal stub tree
# ("Pane" + one "Edit" node at 0,0) instead of real UI elements — not a timing issue,
# confirmed even with the app fully pre-loaded. Needs coordinate-based fallback or
# browser-style automation for these apps; not solved here.

