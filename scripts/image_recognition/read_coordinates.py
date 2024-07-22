import pyautogui
import time

while True:
    try:
        print("Move your mouse to the desired position on the screen.")
        time.sleep(3)  # Gives you 5 seconds to move your mouse to the desired location

        x, y = pyautogui.position()
        print(f"Mouse position: (x={x}, y={y})")

    except Exception as e:
        # Handle the exception (log it, print it, etc.)
        print(f"An error occurred: {e}")
        # Optionally, wait before retrying to avoid a tight loop
        time.sleep(1)
