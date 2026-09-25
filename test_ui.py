from agent.ui import list_ui_elements

import json
import time

from agent.computer import (
    open_app,
    click,
    type_text,
    press_key,
    scroll,
    take_screenshot,
)
open_app("Spotify")
print(json.dumps(list_ui_elements("Spotify"), indent=2))