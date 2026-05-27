import pyautogui
import pytesseract
import time
import json
from rapidfuzz import fuzz

# =========================================
# SETTINGS
# =========================================

MOVE_DURATION = 0.8
TYPE_INTERVAL = 0.05
FUZZ_THRESHOLD = 80

# =========================================
# TEXT VARIATIONS
# =========================================

def generate_text_variants(text):

    return list(set([
        text,
        text.lower(),
        text.upper(),
        text.title()
    ]))


# =========================================
# OCR SEARCH
# =========================================

def find_text_on_screen(target_text, region=None):

    screenshot = pyautogui.screenshot(region=region)

    screenshot = screenshot.resize(
        (screenshot.width * 2, screenshot.height * 2)
    )

    data = pytesseract.image_to_data(
        screenshot,
        output_type=pytesseract.Output.DICT
    )

    variants = generate_text_variants(target_text)

    total = len(data["text"])

    for i in range(total):

        detected_text = data["text"][i].strip()

        if detected_text == "":
            continue

        print("Detected:", detected_text)

        for variant in variants:

            similarity = fuzz.ratio(
                variant.lower(),
                detected_text.lower()
            )

            if similarity >= FUZZ_THRESHOLD:

                x = data["left"][i]
                y = data["top"][i]
                w = data["width"][i]
                h = data["height"][i]

                center_x = (x + w // 2) // 2
                center_y = (y + h // 2) // 2

                if region is not None:

                    center_x += region[0]
                    center_y += region[1]

                return center_x, center_y

    return None


# =========================================
# BASIC ACTIONS
# =========================================

def click_text(text):

    print(f"\nSearching for: {text}")

    result = find_text_on_screen(text)

    if result:

        x, y = result

        pyautogui.moveTo(
            x,
            y,
            duration=MOVE_DURATION
        )

        pyautogui.click()

        print("Clicked!")

        return True

    print("Not found")
    return False


def double_click_text(text):

    success = click_text(text)

    if success:
        pyautogui.doubleClick()


def type_text(text):

    print("Typing:", text)

    pyautogui.write(
        text,
        interval=TYPE_INTERVAL
    )


def press_key(key):

    print("Pressing:", key)

    pyautogui.press(key)


def hotkey(keys):

    print("Hotkey:", keys)

    pyautogui.hotkey(*keys)


# =========================================
# GENERIC REGION OCR ACTION
# =========================================

def find_in_region_and_click(step):

    target_text = step["target_text"]

    region = tuple(step["region"])

    offset_x = step.get("offset_x", 0)
    offset_y = step.get("offset_y", 0)

    print(f"\nSearching in region for: {target_text}")

    result = find_text_on_screen(
        target_text,
        region=region
    )

    if result:

        x, y = result

        x += offset_x
        y += offset_y

        pyautogui.moveTo(
            x,
            y,
            duration=MOVE_DURATION
        )

        pyautogui.click()

        print("Clicked target!")

        return True

    print("Target not found")
    return False


# =========================================
# EXECUTOR
# =========================================

def execute_action(step):

    action = step["action"]

    # -------------------------------------

    if action == "click_text":

        click_text(step["value"])

    # -------------------------------------

    elif action == "double_click_text":

        double_click_text(step["value"])

    # -------------------------------------

    elif action == "type_text":

        type_text(step["value"])

    # -------------------------------------

    elif action == "press_key":

        press_key(step["value"])

    # -------------------------------------

    elif action == "hotkey":

        hotkey(step["value"])

    # -------------------------------------

    elif action == "find_in_region_and_click":

        find_in_region_and_click(step)

    # -------------------------------------

    elif action == "wait":

        time.sleep(step["value"])

    # -------------------------------------

    else:

        print("Unknown action:", action)


# =========================================
# LOAD PLAN
# =========================================

with open("plan.json", "r") as file:

    plan = json.load(file)

# =========================================
# EXECUTE
# =========================================

for step in plan:

    execute_action(step)

print("\nTask Completed!")