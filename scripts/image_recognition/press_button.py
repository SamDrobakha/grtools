import argparse
import pyautogui
import easyocr
import keyboard
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import time
from bidi.algorithm import get_display

# usage example
# sudo python3 press_button.py --num_region 545 571 39 27 --button_location 483 658 --target_number 95 --click_interval 0.5
# to exit press "z"

# Initialize the easyocr reader
reader = easyocr.Reader(['en'])

def read_number_from_screen(region):
    try:
        print("Taking a screenshot of the specified region.")
        # Take a screenshot of the specified region
        screenshot = pyautogui.screenshot(region=region)
        screenshot_path = 'temp.png'
        screenshot.save(screenshot_path)  # Save the screenshot for OCR
        print("Screenshot saved as temp.png.")

        # Open the screenshot using PIL
        with Image.open(screenshot_path) as img:
            print("Opened the screenshot for processing.")
            # Upscale the image to improve OCR accuracy
            img = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)
            print("Upscaled the image.")

            # Convert to grayscale
            img = img.convert('L')
            print("Converted the image to grayscale.")

            # Invert the image to make text black on white
            img = ImageOps.invert(img)
            print("Inverted the image colors.")

            # Enhance the contrast and sharpen the image
            img = ImageEnhance.Contrast(img).enhance(2)
            img = img.filter(ImageFilter.SHARPEN)
            print("Enhanced the contrast and sharpened the image.")

            # Enhance the brightness of the image
            img = ImageEnhance.Brightness(img).enhance(1.5)
            print("Enhanced the brightness of the image.")

            # Save the preprocessed image for inspection
            preprocessed_path = 'temp_processed.png'
            img.save(preprocessed_path)
            print(f"Preprocessed image saved as {preprocessed_path}.")

            # Use easyocr to extract text from the screenshot
            print("Starting OCR with easyocr.")
            result = reader.readtext(preprocessed_path, detail=0)
            print("OCR completed.")
            text = ' '.join(result)
            print(f"OCR Text: '{text}'")

            # Extract the number from the text
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
        # Click the button at the specified location
        pyautogui.click(button_location)
    except Exception as e:
        print(f"An error occurred in press_button: {e}")

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
            # Check if the 'z' key has been pressed
            if keyboard.is_pressed('z'):
                print("Exit key pressed. Exiting loop.")
                break

            # Read the number from the screen
            number = read_number_from_screen(number_region)
            if number is not None:
                print(f"Read number: {number}")
                if number >= target_number:
                    print("Condition met, stopping the script.")
                    break
                else:
                    print("Condition not met, pressing the button again.")
                    press_button(button_location)
                    time.sleep(click_interval)  # Wait briefly before the next click
            else:
                print("Failed to read number, trying again.")
                time.sleep(click_interval)

            # Reduce sleep time and increase frequency of key press checking
            for _ in range(int(click_interval * 10)):  # Check frequently in the interval
                if keyboard.is_pressed('z'):
                    print("Exit key pressed. Exiting loop.")
                    break
                time.sleep(0.1)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
