#!/usr/bin/env python

# To check
# python -c "import torch; print(torch.__version__)"
# python -c "import easyocr; print('EasyOCR installed successfully')"

# To Run
# python3 press_button.py --num_region 545 571 39 27 --button_location 483 658 --target_number 90 --click_interval 0.05
# to exit press "enter"

import argparse
import pyautogui
import easyocr
import sys
import select
import time
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

# Initialize the easyocr reader
reader = easyocr.Reader(['en'])

def read_number_from_screen(region):
    try:
        print("Taking a screenshot of the specified region.")
        screenshot = pyautogui.screenshot(region=region)
        screenshot_path = 'temp.png'
        screenshot.save(screenshot_path)
        print("Screenshot saved as temp.png.")

        with Image.open(screenshot_path) as img:
            print("Processing image...")
            img = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)
            img = img.convert('L')
            img = ImageOps.invert(img)
            img = ImageEnhance.Contrast(img).enhance(2)
            img = img.filter(ImageFilter.SHARPEN)
            img = ImageEnhance.Brightness(img).enhance(1.5)

            preprocessed_path = 'temp_processed.png'
            img.save(preprocessed_path)
            print(f"Preprocessed image saved as {preprocessed_path}.")

            print("Starting OCR with easyocr.")
            result = reader.readtext(preprocessed_path, detail=0)
            print("OCR completed.")
            text = ' '.join(result)
            print(f"OCR Text: '{text}'")

            number = int(''.join(filter(str.isdigit, text)))
            return number
    except ValueError:
        print("ValueError: No valid number found in OCR text.")
        return None
    except Exception as e:
        print(f"An error occurred in read_number_from_screen: {e}")
        return None

def press_button(button_location):
    try:
        print(f"Clicking the button at location {button_location}.")
        pyautogui.click(button_location)
    except Exception as e:
        print(f"An error occurred in press_button: {e}")

def check_exit_key():
    """Check for user input to exit the script."""
    i, o, e = select.select([sys.stdin], [], [], 0.1)  # Non-blocking input check
    return bool(i)

def main():
    parser = argparse.ArgumentParser(description="Automate button pressing based on screen OCR.")
    parser.add_argument('--num_region', type=int, nargs=4, required=True, 
                        help="Region to capture the number as x y width height")
    parser.add_argument('--button_location', type=int, nargs=2, required=True, 
                        help="Location of the button as x y")
    parser.add_argument('--target_number', type=int, required=True, 
                        help="The target number to achieve before stopping")
    parser.add_argument('--click_interval', type=float, default=0.5, 
                        help="Interval between clicks in seconds (default: 0.5s)")
    args = parser.parse_args()

    number_region = tuple(args.num_region)
    button_location = tuple(args.button_location)
    target_number = args.target_number
    click_interval = args.click_interval

    try:
        while True:
            if check_exit_key():
                print("Exit key pressed. Exiting loop.")
                break

            number = read_number_from_screen(number_region)
            if number is not None:
                print(f"Read number: {number}")
                if number >= target_number:
                    print("Condition met, stopping the script.")
                    break
                else:
                    print("Condition not met, pressing the button again.")
                    press_button(button_location)
                    time.sleep(click_interval)
            else:
                print("Failed to read number, trying again.")
                time.sleep(click_interval)

            # Reduce sleep time and increase frequency of key press checking
            for _ in range(int(click_interval * 10)):  # Frequent checking in the interval
                if check_exit_key():
                    print("Exit key pressed. Exiting loop.")
                    return  # Use `return` to exit the function immediately
                time.sleep(0.1)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()