import pyautogui
import pytesseract
import time

# ----------------------------------------
# SETTINGS
# ----------------------------------------

START_DELAY = 5
MOVE_DURATION = 1
TYPE_INTERVAL = 0.08

# ----------------------------------------
# OCR CLICK FUNCTION
# ----------------------------------------

def click_text(target_text):

    print(f"\nSearching for: {target_text}")

    # Screenshot
    screenshot = pyautogui.screenshot()

    # Upscale for better OCR
    screenshot = screenshot.resize(
        (screenshot.width * 2, screenshot.height * 2)
    )

    # OCR
    data = pytesseract.image_to_data(
        screenshot,
        output_type=pytesseract.Output.DICT
    )

    total = len(data["text"])

    for i in range(total):

        text = data["text"][i].strip().lower()

        if text == "":
            continue

        print("Detected:", text)

        # Semantic partial match
        if target_text.lower() in text:

            x = data["left"][i]
            y = data["top"][i]
            w = data["width"][i]
            h = data["height"][i]

            # Correct coordinates after upscale
            center_x = (x + w // 2) // 2
            center_y = (y + h // 2) // 2

            print("Match found!")
            print("Coordinates:", center_x, center_y)

            # Human-like move
            pyautogui.moveTo(
                center_x,
                center_y,
                duration=MOVE_DURATION
            )

            time.sleep(0.5)

            pyautogui.click()

            return True

    return False

# ----------------------------------------
# MAIN FLOW
# ----------------------------------------

print(f"Starting in {START_DELAY} seconds...")
time.sleep(START_DELAY)

# ----------------------------------------
# STEP 1 — OPEN CHROME
# ----------------------------------------

success = click_text("brave")

if not success:
    print("Chrome not found")
    exit()

pyautogui.doubleClick()

print("Opening Chrome...")
time.sleep(3)

# ----------------------------------------
# STEP 2 — OPEN YOUTUBE
# ----------------------------------------

pyautogui.write(
    "youtube.com",
    interval=TYPE_INTERVAL
)

pyautogui.press("enter")

print("Opening YouTube...")
time.sleep(5)

# ----------------------------------------
# STEP 3 — SEARCH MACARENA
# ----------------------------------------

# Click search box
success = click_text("Search")

if not success:
    print("Search bar not found")
    exit()

time.sleep(1)

# Type song name
pyautogui.write(
    "macarena",
    interval=TYPE_INTERVAL
)

pyautogui.press("enter")

print("Searching...")
time.sleep(5)


# ----------------------------------------
# STEP 4 — CLICK FIRST VIDEO USING IMAGE REGION
# ----------------------------------------

time.sleep(5)

# Get screen size
screen_width, screen_height = pyautogui.size()

# YouTube videos usually appear below top navbar
# Ignore top area to avoid tabs/search bar

search_region = (
    0,                      # x
    200,                    # y start
    screen_width,           # width
    screen_height - 200     # height
)

# Screenshot only video area
screenshot = pyautogui.screenshot(region=search_region)

# Upscale for OCR
screenshot = screenshot.resize(
    (screenshot.width * 2, screenshot.height * 2)
)

# OCR
data = pytesseract.image_to_data(
    screenshot,
    output_type=pytesseract.Output.DICT
)

found = False

for i in range(len(data["text"])):

    text = data["text"][i].strip().lower()

    if "macarena" in text:

        x = data["left"][i]
        y = data["top"][i]
        w = data["width"][i]
        h = data["height"][i]

        # Convert back after upscale
        center_x = (x + w // 2) // 2
        center_y = (y + h // 2) // 2

        # Add region offset back
        actual_x = center_x
        actual_y = center_y + 200

        print("Video title found")

        # Move slightly left toward thumbnail
        thumbnail_x = actual_x - 250
        thumbnail_y = actual_y

        pyautogui.moveTo(
            thumbnail_x,
            thumbnail_y,
            duration=1
        )

        time.sleep(0.5)

        pyautogui.click()

        found = True
        break

if not found:
    print("Video not found")