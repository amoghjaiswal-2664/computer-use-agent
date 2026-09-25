from agent import computer
from agent import ui

tools = [
    {
        "type": "function",
        "function": {
            "name": "open_app",
            "description": "Open an application, file, folder, URL, or other target using Windows. The argument is not limited to application names and can be an application name such as 'notepad' or 'spotify', a full folder path such as r'D:\\movies', a full file path such as r'D:\\movies\\movie.mp4', or a URL such as 'https://youtube.com'. Windows determines how to open the supplied target; for example, a folder path opens that folder directly in File Explorer. Use this tool to directly open a known target instead of manually navigating through File Explorer. Returns True if the launch command was successfully issued and False if an error occurred.",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {
                        "type": "string",
                        "description": "he application name, file path, folder path, or URL to open, e.g. 'notepad', r'D:\\movies', or 'https://youtube.com'."
                    }
                },
                "required": ["app_name"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "list_ui_elements",
            "description": "Find a visible Windows window whose title contains the given substring and return its labeled UI elements. Each returned element contains: name (visible text), control_type (Windows UI control type), x/y (center coordinates usable with the click tool). Use this to inspect a window before interacting with buttons, text fields, menus, or labeled controls. Uses Windows UI Automation (UIA) — works reliably with native Windows apps, but Electron/Chromium apps may expose few or inaccurate elements; if that happens, fall back to coordinate-based clicking from a screenshot. Waits up to `timeout` seconds for the window/elements to become available.",
            "parameters": {
                "type": "object",
                "properties": {
                        "window_title_substr": {
                        "type": "string",
                        "description": "A distinctive substring of the target window's title, e.g. 'Spotify' or 'File Explorer'."
                    }
                },
                "required": ["window_title_substr"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "click",
            "description": "Click the left mouse button at the specified absolute Windows screen coordinates. Use this tool to interact with visible UI elements when their coordinates are known, such as coordinates returned by list_ui_elements() or determined from a screenshot.",
            "parameters": {
                "type": "object",
                "properties": {
                    "x": {
                        "type": "integer",
                        "description": "The horizontal screen coordinate (X position) where the mouse should click."
                    },
                    "y": {
                        "type": "integer",
                        "description": "The vertical screen coordinate (Y position) where the mouse should click."
                    }
                },
                "required": ["x", "y"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "type_text",
            "description": "Type the given text into the currently focused application or input field using simulated keyboard input. The target window or text field must already have focus. Use this for entering paths, search queries, filenames, commands, form data, and other keyboard-accessible text. The interval controls the delay between typed characters.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to type."
                    },
                    "interval": {
                        "type": "number",
                        "description": "The delay in seconds between each typed character. Defaults to 0.02."
                    }
                },
                "required": ["text"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "press_key",
            "description": "Press a keyboard key in the currently focused application. Examples include 'enter', 'esc', 'tab', 'backspace', 'ctrl', 'shift', 'alt', 'space', 'up', 'down', 'left', and 'right'. Use this for keyboard shortcuts, submitting dialogs, navigating fields, closing menus, and other keyboard interactions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": "The keyboard key to press, e.g. 'enter', 'esc', 'tab', 'space', or 'backspace'."
                    }
                },
                "required": ["key"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "scroll",
            "description": "Scroll the mouse wheel at the current cursor position. Positive values scroll upward and negative values scroll downward. Use this to navigate vertically through windows, webpages, lists, File Explorer folders, and other scrollable interfaces.",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "integer",
                        "description": "The number of scroll units. Positive values scroll up, negative values scroll down."
                    }
                },
                "required": ["amount"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "take_screenshot",
            "description": "Capture the current screen and save it to the specified image path. Returns the path of the saved screenshot. Use this when visual information is needed to determine the current UI state, locate elements that are not exposed through UI Automation, verify whether an action succeeded, or determine coordinates for click().",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The file path where the screenshot should be saved. Defaults to 'screenshot.png'."
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "double_click",
            "description": "Double-click the left mouse button at the specified screen coordinates. Use this tool when an interface requires a double-click, such as opening a file or folder, launching an item, or interacting with an element that responds to double-clicks. Coordinates are measured in pixels from the top-left corner of the screen, where (0, 0) is the top-left. The x coordinate increases from left to right and the y coordinate increases from top to bottom. The coordinates must be within the current screen bounds. Returns a success message if the double-click was performed, or an error message if the coordinates are outside the screen bounds.",
            "parameters": {
                "type": "object",
                "properties": {
                    "x": {
                        "type": "integer",
                        "description": "The horizontal screen coordinate in pixels, measured from the left edge of the screen. Must be within the current screen width."
                    },
                    "y": {
                        "type": "integer",
                        "description": "The vertical screen coordinate in pixels, measured from the top edge of the screen. Must be within the current screen height."
                    }
                },
                "required": ["x", "y"],
            },
        },
    },
]


DISPATCH = {
    "open_app": computer.open_app,
    "click": computer.click,
    "type_text": computer.type_text,
    "press_key": computer.press_key,
    "scroll": computer.scroll,
    "take_screenshot": computer.take_screenshot,
    "list_ui_elements": ui.list_ui_elements,
    "double_click": computer.double_click,
}

def call_tool(name: str, arguments: dict):
    if name not in DISPATCH:
        raise ValueError(f"Unknown tool: {name}")
    return DISPATCH[name](**arguments)
