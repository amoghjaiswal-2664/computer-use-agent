import time

from agent.computer import (
    open_app,
    click,
    type_text,
    press_key,
    scroll,
    take_screenshot,
)


print("Starting computer.py tests...")
print()


# 1. Test open_app()
print("TEST 1: Opening Notepad...")
result = open_app("spotifyHello! EDEN computer control is working.")
print("Result:", result)

time.sleep(2)


# 2. Test type_text()
print("TEST 2: Typing text...")
type_text("Hello! EDEN computer control is working.")
time.sleep(1)


# 3. Test press_key()
print("TEST 3: Pressing Enter...")
press_key("enter")
type_text("This text was typed after pressing Enter.")
time.sleep(1)


# 4. Test click()
print("TEST 4: Testing mouse click...")
print("Move your mouse to a safe location if needed.")
time.sleep(2)

click(500, 500)
time.sleep(1)


# 5. Test scroll()
print("TEST 5: Testing scroll...")
scroll(-5)
time.sleep(1)


# 6. Test take_screenshot()
print("TEST 6: Taking screenshot...")
path = take_screenshot("test_screenshot.png")
print("Screenshot saved to:", path)


print()
print("All tests completed!")