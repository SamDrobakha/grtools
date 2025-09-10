#!/usr/bin/env python

# instructions how to use
# conda activate pytorch_env
# python3 press_button.py --num_region 545 571 39 27 --button_location 483 658 --target_number 95 --click_interval 0.01 --second_button_location 483 700

import argparse
import pyautogui
import easyocr
import sys
import select
import time
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

# Optional Tesseract fallback
try:
    import pytesseract
    _HAS_TESSERACT = True
except Exception:
    _HAS_TESSERACT = False

# Optional NumPy for segmentation fallback
try:
    import numpy as np
    _HAS_NUMPY = True
except Exception:
    _HAS_NUMPY = False

# Optional OpenCV for robust binarization
try:
    import cv2
    _HAS_CV2 = True
except Exception:
    _HAS_CV2 = False

# Initialize the easyocr reader
reader = easyocr.Reader(['en'])

# Global defaults (tunable via CLI)
SCALE_FACTOR = 3.0
MAX_DIGITS = None  # set via CLI to constrain output length

def _normalize_digits(digits: str) -> str:
    """Clamp the recognized digits to the configured MAX_DIGITS (keep rightmost)."""
    if not digits:
        return ''
    if MAX_DIGITS is not None and len(digits) > MAX_DIGITS:
        return digits[-MAX_DIGITS:]
    return digits

def read_number_from_screen(region, debug=True):
    try:
        screenshot = pyautogui.screenshot(region=region)
        screenshot_path = 'temp.png'
        screenshot.save(screenshot_path)

        with Image.open(screenshot_path) as img:
            # Upscale and convert to grayscale
            base = img.resize((int(img.width * SCALE_FACTOR), int(img.height * SCALE_FACTOR)), Image.LANCZOS).convert('L')

            # Preprocessing helper (optionally invert first)
            def preprocess(image, invert=False):
                work = ImageOps.invert(image) if invert else image
                work = ImageEnhance.Contrast(work).enhance(3.0)
                work = ImageEnhance.Brightness(work).enhance(2.0)
                work = work.filter(ImageFilter.SHARPEN)
                work = work.filter(ImageFilter.EDGE_ENHANCE)
                return work

            img_proc_inv = preprocess(base, invert=True)
            img_proc = preprocess(base, invert=False)

            # Save both variants for inspection
            inv_path = 'temp_processed.png'
            norm_path = 'temp_processed_alt.png'
            img_proc_inv.save(inv_path)
            img_proc.save(norm_path)

            # Try EasyOCR: inverted first, then non-inverted, with a digit allowlist if supported
            for pth in (inv_path, norm_path):
                try:
                    result = reader.readtext(pth, detail=0, allowlist="0123456789")
                except TypeError:
                    # Older EasyOCR versions may not support allowlist
                    result = reader.readtext(pth, detail=0)
                text = ' '.join(result) if result else ''
                digits = _normalize_digits(''.join(filter(str.isdigit, text)))
                if digits:
                    return int(digits)

            # Optional fallback: Tesseract (if available)
            if '_HAS_TESSERACT' in globals() and _HAS_TESSERACT:
                for im in (img_proc_inv, img_proc):
                    try:
                        t_text = pytesseract.image_to_string(
                            im, config="--psm 7 -c tessedit_char_whitelist=0123456789"
                        )
                        digits = _normalize_digits(''.join(filter(str.isdigit, t_text)))
                        if digits:
                            return int(digits)
                    except Exception:
                        pass

            # Segmentation fallback: split into digit regions and OCR each separately
            if '_HAS_NUMPY' in globals() and _HAS_NUMPY:
                try:
                    # Use non-inverted processed image as base for segmentation
                    seg_src = img_proc.copy().convert('L')
                    arr = np.array(seg_src)

                    # Binarize: prefer Otsu via OpenCV if available; fallback to adaptive threshold
                    if '_HAS_CV2' in globals() and _HAS_CV2:
                        try:
                            # THRESH_BINARY_INV so digits become 1s
                            _, bin_img = cv2.threshold(arr, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
                            bin_arr = (bin_img // 255).astype(np.uint8)
                        except Exception:
                            thr = max(64, int(arr.mean()))
                            bin_arr = (arr < thr).astype(np.uint8)
                    else:
                        thr = max(64, int(arr.mean()))
                        bin_arr = (arr < thr).astype(np.uint8)

                    # Vertical projection to find gaps between digits
                    col_sums = bin_arr.sum(axis=0)
                    # Consider a column a gap if it has very few stroke pixels
                    gap_threshold = max(1, int(0.02 * bin_arr.shape[0]))
                    gap = col_sums <= gap_threshold

                    # Find contiguous non-gap runs (potential digit regions)
                    segments = []
                    in_run = False
                    start = 0
                    for i, g in enumerate(gap):
                        if not in_run and not g:
                            in_run = True
                            start = i
                        elif in_run and g:
                            end = i
                            if end - start >= 4:  # ignore tiny noise
                                segments.append((start, end))
                            in_run = False
                    if in_run:
                        end = len(gap)
                        if end - start >= 4:
                            segments.append((start, end))

                    # Merge segments separated by tiny gaps (likely same digit split)
                    merged = []
                    for seg in segments:
                        if not merged:
                            merged.append(list(seg))
                        else:
                            prev = merged[-1]
                            # If the gap between prev and seg is very small relative to height, merge
                            small_gap = seg[0] - prev[1] <= max(2, int(0.01 * bin_arr.shape[0]))
                            if small_gap:
                                prev[1] = seg[1]
                            else:
                                merged.append(list(seg))
                    segments = [tuple(x) for x in merged]

                    # If we found at least 2 segments, OCR each as a single digit
                    if len(segments) >= 2:
                        digits_out = []
                        for (l, r) in segments:
                            pad = 2
                            l0 = max(0, l - pad)
                            r0 = min(seg_src.width, r + pad)
                            crop = seg_src.crop((l0, 0, r0, seg_src.height))

                            # Prefer Tesseract single-char mode if available
                            d = ''
                            if '_HAS_TESSERACT' in globals() and _HAS_TESSERACT:
                                try:
                                    d = pytesseract.image_to_string(
                                        crop, config="--psm 10 -c tessedit_char_whitelist=0123456789"
                                    ).strip()
                                except Exception:
                                    d = ''
                            if not d:
                                # EasyOCR as fallback on small crop
                                try:
                                    res = reader.readtext(crop, detail=0, allowlist="0123456789")
                                except TypeError:
                                    res = reader.readtext(crop, detail=0)
                                d = ''.join(filter(str.isdigit, ''.join(res))) if res else ''

                            if d:
                                digits_out.append(d[0])

                        if digits_out:
                            try:
                                assembled = ''.join(digits_out)
                                if MAX_DIGITS is not None and len(assembled) > MAX_DIGITS:
                                    assembled = assembled[-MAX_DIGITS:]
                                return int(assembled)
                            except Exception:
                                pass
                except Exception:
                    pass

            if debug:
                print("OCR failed; saved temp.png, temp_processed.png, temp_processed_alt.png for inspection.")
                try:
                    img_proc_inv.show()
                except Exception:
                    pass
            return None
    except Exception as e:
        print(f"Error in read_number_from_screen: {e}")
        return None

def press_button(button_location):
    try:
        pyautogui.click(button_location)
    except Exception as e:
        print(f"Error in press_button: {e}")

def check_exit_key():
    i, o, e = select.select([sys.stdin], [], [], 0.1)
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
    parser.add_argument('--second_button_location', type=int, nargs=2, required=True,
                        help="Location of the second button as x y when number increases")
    parser.add_argument('--debug', action='store_true',
                        help="Show processed images and keep temp files on OCR failure")
    parser.add_argument('--scale', type=float, default=3.0,
                        help='Upscale factor before OCR (default: 3.0)')
    parser.add_argument('--max_digits', type=int, default=None,
                        help='If set, limit recognized number to the rightmost N digits')
    args = parser.parse_args()

    debug = args.debug

    global SCALE_FACTOR, MAX_DIGITS
    SCALE_FACTOR = max(1.0, float(args.scale))
    MAX_DIGITS = args.max_digits if args.max_digits is not None else len(str(args.target_number))

    number_region = tuple(args.num_region)
    button_location = tuple(args.button_location)
    second_button_location = tuple(args.second_button_location)
    target_number = args.target_number
    click_interval = args.click_interval
    
    max_saved_number = 0  # Stores the highest number found

    try:
        while True:
            if check_exit_key():
                print("Exit key pressed. Exiting loop.")
                break

            if number_region[2] < 20 or number_region[3] < 15:
                print(f"Warning: capture region is small ({number_region[2]}x{number_region[3]}). Try increasing --scale or enlarging --num_region.")

            number = read_number_from_screen(number_region, debug=debug)
            if number is not None:
                print(f"Read number: {number}")
                print(f"Current highest recorded number: {max_saved_number}")  # Always display max value
                
                if number > max_saved_number:
                    print(f"New highest number found: {number} (previous: {max_saved_number}). Clicking second button.")
                    press_button(second_button_location)
                    max_saved_number = number  # Update the highest recorded value
                
                if number >= target_number:
                    print("Condition met, stopping the script.")
                    break
                else:
                    print("Condition not met, pressing the primary button again.")
                    press_button(button_location)
                    time.sleep(click_interval)
            else:
                print("Failed to read number, trying again.")
                time.sleep(click_interval)

            for _ in range(int(click_interval * 10)):
                if check_exit_key():
                    print("Exit key pressed. Exiting loop.")
                    return
                time.sleep(0.1)
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
