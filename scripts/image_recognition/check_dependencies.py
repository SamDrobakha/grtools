import importlib.util

def check_module(module_name):
    spec = importlib.util.find_spec(module_name)
    if spec is not None:
        print(f"'{module_name}' is installed at: {spec.origin}")
    else:
        print(f"'{module_name}' is not installed.")

check_module('easyocr')
check_module('numpy')
check_module('pyautogui')
check_module('torch')
check_module('keyboard')
check_module('bidi.algorithm')

print("Dependency check completed.")
