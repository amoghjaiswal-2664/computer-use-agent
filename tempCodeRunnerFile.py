import time
from agent.computer import(
    open_app,
    click,
    type_text,
    press_key,
    scroll,
    take_screenshot,
)

#1
print("Test 1 starting")
result = open_app("Notepad")
print("result:",result)
time.sleep(2)
#2 
print("Test 2 starting")
time.sleep(2)
click(500,500)
time.sleep(1)
#3
print("Test 3 type_text")
type_text("Hello! EDEN computer control is working.")
time.sleep(2)
#4
print("Test 4 press_key")
press_key("enter")
type_text("This text was typed after pressing Enter.")
time.sleep(2)
#5
print("Test 5 scroll")
scroll(-5)
time.sleep(1)
#6
print("Test 6 take_screenshot")
path = take_screenshot("test_screenshot.png")
print("Screenshot saved to:", path)


print()
print("All tests completed!")