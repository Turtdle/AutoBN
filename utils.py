import pyautogui
import time
import random
from typing import Callable, Union, Tuple, Literal
from PIL import Image, ImageDraw
import numpy as np

DIAMOND_COORDS = [
    {
        "top": (1022, 264),
        "left": (815, 367),
        "right": (1229, 367),
        "bottom": (1022, 471),
    },
    {
        "top": (1229, 368),
        "left": (1022, 471),
        "right": (1436, 471),
        "bottom": (1229, 575),
    },
    {
        "top": (1436, 472),
        "left": (1229, 575),
        "right": (1643, 575),
        "bottom": (1436, 679),
    },
    {
        "top": (1643, 576),
        "left": (1436, 679),
        "right": (1850, 679),
        "bottom": (1643, 783),
    },
    {
        "top": (1850, 680),
        "left": (1643, 783),
        "right": (2057, 783),
        "bottom": (1850, 887),
    },
    {
        "top": (1228, 160),
        "left": (1021, 263),
        "right": (1435, 263),
        "bottom": (1228, 367),
    },
    {
        "top": (1436, 264),
        "left": (1229, 367),
        "right": (1643, 367),
        "bottom": (1436, 471),
    },
    {
        "top": (1643, 368),
        "left": (1436, 471),
        "right": (1850, 471),
        "bottom": (1643, 575),
    },
    {
        "top": (1850, 472),
        "left": (1643, 575),
        "right": (2057, 575),
        "bottom": (1850, 679),
    },
    {
        "top": (2057, 576),
        "left": (1850, 679),
        "right": (2264, 679),
        "bottom": (2057, 783),
    },
    {
        "top": (1642, 160),
        "left": (1435, 263),
        "right": (1849, 263),
        "bottom": (1642, 367),
    },
    {
        "top": (1849, 264),
        "left": (1642, 367),
        "right": (2056, 367),
        "bottom": (1849, 471),
    },
    {
        "top": (2056, 368),
        "left": (1849, 471),
        "right": (2263, 471),
        "bottom": (2056, 575),
    },
]


def precise_click(*args):
    if len(args) == 1:
        location = args[0]
    elif len(args) == 2:
        location = args
    else:
        raise ValueError("Pass either a tuple (x, y) or two separate coordinates x, y")

    pyautogui.mouseDown(location)
    time.sleep(random.uniform(0.09, 0.11))
    pyautogui.mouseUp(location)


def battle_done(screenshot=True):
    time.sleep(0.5)
    pyautogui.click(1570, 1031)
    if screenshot:
        pyautogui.screenshot("shared_folder/screenshot.png")
    time.sleep(0.5)
    pyautogui.click(1570, 1031)


def remove_stop():
    import os

    # Windows path (backslashes) - adjust to match your screenshot folder
    stop_file_path = "shared_folder\\stop.txt"

    # Alternative: forward slashes also work on Windows
    # stop_file_path = "shared_folder/stop.txt"

    if os.path.exists(stop_file_path):
        try:
            # Delete the stop file so it only triggers once
            os.remove(stop_file_path)
            print("Stop signal detected - stop.txt found and removed")
            return True
        except Exception as e:
            print(f"Error removing stop.txt: {e}")
            return True  # Still signal to stop even if we can't delete

    return False


def check_for_stop():
    """Check if stop.txt file exists, delete it if found, and return True if stopping"""
    import os

    # Windows path (backslashes) - adjust to match your screenshot folder
    stop_file_path = "shared_folder\\stop.txt"

    # Alternative: forward slashes also work on Windows
    # stop_file_path = "shared_folder/stop.txt"

    if os.path.exists(stop_file_path):
        try:
            # Delete the stop file so it only triggers once
            # os.remove(stop_file_path)
            print("Stop signal detected - stop.txt found and removed")
            return True
        except Exception as e:
            print(f"Error removing stop.txt: {e}")
            return True  # Still signal to stop even if we can't delete

    return False


def retry_until(
    click_input: Union[Callable[[], None], int, Tuple[int, int]],
    y_or_check: Union[int, Callable[[], bool], None] = None,
    check_function: Union[Callable[[], bool], None] = None,
    retry_time: int = 20,
) -> bool:
    """
    Flexible retry function that accepts multiple input formats for clicking
    Usage patterns:
        retry_button(lambda: pyautogui.click(100, 200), check_func)
        retry_button(100, 200, check_func)
        retry_button((100, 200), check_func)
    Args:
        click_input: Lambda function, x coordinate, or (x,y) tuple
        y_or_check: Y coordinate (if click_input is x) OR check function (if click_input is lambda/tuple)
        check_function: Check function (only needed if using x,y coordinates)
        retry_time (int): Total time in seconds to keep retrying (default: 20)
    Returns:
        bool: True if check_function eventually returned True, False if timeout
    """
    if callable(click_input):
        click_func = click_input
        click_description = "lambda function"
        if callable(y_or_check):
            check_func = y_or_check
        else:
            raise ValueError(
                "When using lambda, second parameter must be check_function"
            )
    elif isinstance(click_input, tuple):
        x, y = click_input
        click_description = f"coordinates ({x}, {y})"

        def click_func():
            precise_click((x, y))

        if callable(y_or_check):
            check_func = y_or_check
        else:
            raise ValueError(
                "When using tuple, second parameter must be check_function"
            )
    elif isinstance(click_input, int):
        x = click_input
        if isinstance(y_or_check, int):
            y = y_or_check
            click_description = f"coordinates ({x}, {y})"

            def click_func():
                precise_click((x, y))

            if callable(check_function):
                check_func = check_function
            else:
                raise ValueError(
                    "When using x,y coordinates, check_function must be provided"
                )
        else:
            raise ValueError(
                "When providing x coordinate, y coordinate must be provided as second parameter"
            )
    else:
        raise ValueError(
            "First parameter must be a lambda function, x coordinate (int), or (x,y) tuple"
        )

    check_name = getattr(check_func, "__name__", "check function")
    print(f"Retrying click on {click_description} until {check_name} returns True")

    start_time = time.time()
    attempt = 1

    while time.time() - start_time < retry_time:
        print(f"Attempt {attempt}: Clicking {click_description}")
        click_func()
        time.sleep(0.1)

        if check_func():
            print(f"Success! {check_name} returned True after {attempt} attempt(s)")
            return True

        print(f"{check_name} didn't trigger, retrying...")
        time.sleep(1)
        attempt += 1

    elapsed_time = time.time() - start_time
    print(
        f"Time limit reached ({elapsed_time:.1f}s) for clicking {click_description} until {check_name}"
    )
    return False


def check_win(
    top_left_x=1049,
    top_left_y=784,
    bottom_right_x=1071,
    bottom_right_y=819,
    target_color=(165, 161, 149),
    tolerance=100,
):
    width = bottom_right_x - top_left_x
    height = bottom_right_y - top_left_y

    screenshot = pyautogui.screenshot(region=(top_left_x, top_left_y, width, height))

    if screenshot.mode != "RGB":
        screenshot = screenshot.convert("RGB")

    pixels = list(screenshot.getdata())

    for pixel in pixels:
        if not (
            abs(pixel[0] - target_color[0]) <= tolerance
            and abs(pixel[1] - target_color[1]) <= tolerance
            and abs(pixel[2] - target_color[2]) <= tolerance
        ):
            return False

    return True


def check_turn():
    return pyautogui.pixel(220, 346) == (191, 95, 7)


def look_for_image(image_name: str, _confidence=0.8):
    """
    Looks for a image on screen
    Args:
        image_name : str of image name icluding file extension

    Returns:
        Pixel location or None
    """
    try:
        location = pyautogui.locateOnScreen(
            f"./images/{image_name}", grayscale=True, confidence=_confidence
        )
        if location:
            print(f"Found at: {location}")
            return location
    except pyautogui.ImageNotFoundException:
        print("Image not found on screen")
        return None


def look_for_image_with_wait(image_name: str, _confidence=0.8, wait=20):
    """
    Looks for a image on screen
    Args:
        image_name : str of image name icluding file extension

    Returns:
        Pixel location or None
    """
    for _i in range(wait):
        a = look_for_image(image_name=image_name, _confidence=0.8)
        if not a:
            time.sleep(1)
        else:
            return a


def click_generic_middle_enemy():
    precise_click((1400, 575))


def select_unit_slot(slot: int, return_coords=False):
    """
    selects a unit on grid:

    1 2 3 4 5
    6 7 8 9 10
     11 12 13

    param: slot
        num 1-13

    return:
        None
    """
    loc = None
    if slot == 1:
        loc = (704, 511)
    if slot == 2:
        loc = (916, 610)
    if slot == 3:
        loc = (1118, 709)
    if slot == 4:
        loc = (1315, 803)
    if slot == 5:
        loc = (1516, 919)
    if slot == 6:
        loc = (495, 621)
    if slot == 7:
        loc = (721, 736)
    if slot == 8:
        loc = (898, 816)
    if slot == 9:
        loc = (1122, 926)
    if slot == 10:
        loc = (1340, 1042)
    if slot == 11:
        loc = (498, 830)
    if slot == 12:
        loc = (683, 931)
    if slot == 13:
        loc = (900, 1044)
    if return_coords:
        return loc
    else:
        precise_click(loc)
        return None


def check_select():
    hex_color = "ffffff"
    target_rgb = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return pyautogui.pixel(2422, 900) == target_rgb


def scroll_down_fast():
    for i in range(150):
        pyautogui.scroll(-10, _pause=False)


def scroll_up_fast():
    for i in range(150):
        pyautogui.scroll(10, _pause=False)


def wait_for_atk_button():
    hex_color = "73e609"
    target_rgb = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return pyautogui.pixel(2462, 1324) == target_rgb


def click_all_front_row():
    pyautogui.mouseDown(1000, 350)
    time.sleep(random.uniform(0.009, 0.011))
    pyautogui.mouseUp(1000, 350)
    time.sleep(0.005)

    pyautogui.mouseDown(1200, 450)
    time.sleep(random.uniform(0.009, 0.011))
    pyautogui.mouseUp(1200, 450)
    time.sleep(0.005)

    pyautogui.mouseDown(1400, 575)
    time.sleep(random.uniform(0.009, 0.011))
    pyautogui.mouseUp(1400, 575)
    time.sleep(0.005)
    #
    pyautogui.mouseDown(1650, 650)
    time.sleep(random.uniform(0.009, 0.011))
    pyautogui.mouseUp(1650, 650)
    time.sleep(0.005)

    pyautogui.mouseDown(1850, 750)
    time.sleep(random.uniform(0.009, 0.011))
    pyautogui.mouseUp(1850, 750)


def select_ability(ability_number: Literal[1, 2, 3]):
    if ability_number == 1:
        precise_click(564, 1335)
    elif ability_number == 2:
        precise_click(750, 1335)
    elif ability_number == 3:
        precise_click(950, 1335)
    else:
        raise ValueError


def diamond_screenshot(
    top_x, top_y, left_x, left_y, right_x, right_y, bottom_x, bottom_y
):
    # Calculate bounding box for the diamond
    min_x = min(top_x, left_x, right_x, bottom_x)
    max_x = max(top_x, left_x, right_x, bottom_x)
    min_y = min(top_y, left_y, right_y, bottom_y)
    max_y = max(top_y, left_y, right_y, bottom_y)
    width = max_x - min_x
    height = max_y - min_y

    # Take rectangular screenshot of the bounding area
    screenshot = pyautogui.screenshot(region=(min_x, min_y, width, height))
    screenshot = screenshot.convert("RGB")

    # Create diamond mask
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)

    # Convert absolute coordinates to relative coordinates within the bounding box
    diamond_points = [
        (top_x - min_x, top_y - min_y),  # top
        (right_x - min_x, right_y - min_y),  # right
        (bottom_x - min_x, bottom_y - min_y),  # bottom
        (left_x - min_x, left_y - min_y),  # left
    ]

    # Draw diamond shape
    draw.polygon(diamond_points, fill=255)

    # Apply mask to screenshot
    screenshot.putalpha(mask)

    # Convert back to RGB (removes alpha channel, sets transparent areas to white)
    rgb_screenshot = Image.new("RGB", screenshot.size, (255, 255, 255))
    rgb_screenshot.paste(
        screenshot, mask=screenshot.split()[-1] if screenshot.mode == "RGBA" else None
    )

    return rgb_screenshot


def get_diamond_mask(coords, width, height, min_x, min_y):
    """Create a mask for the diamond shape"""
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)

    diamond_points = [
        (coords["top"][0] - min_x, coords["top"][1] - min_y),
        (coords["right"][0] - min_x, coords["right"][1] - min_y),
        (coords["bottom"][0] - min_x, coords["bottom"][1] - min_y),
        (coords["left"][0] - min_x, coords["left"][1] - min_y),
    ]

    draw.polygon(diamond_points, fill=255)
    return mask


def calculate_diamond_average_color(diamond_img, coords):
    """Calculate average color of only the diamond pixels"""
    # Get bounding box dimensions
    min_x = min(
        coords["top"][0], coords["left"][0], coords["right"][0], coords["bottom"][0]
    )
    max_x = max(
        coords["top"][0], coords["left"][0], coords["right"][0], coords["bottom"][0]
    )
    min_y = min(
        coords["top"][1], coords["left"][1], coords["right"][1], coords["bottom"][1]
    )
    max_y = max(
        coords["top"][1], coords["left"][1], coords["right"][1], coords["bottom"][1]
    )

    width = max_x - min_x
    height = max_y - min_y

    # Create mask and get diamond pixels only
    mask = get_diamond_mask(coords, width, height, min_x, min_y)
    img_array = np.array(diamond_img)
    mask_array = np.array(mask)

    diamond_pixels = img_array[mask_array > 0]
    return np.mean(diamond_pixels, axis=0)


def select_enemy_slot(slot: int, return_coords=False):
    """
    selects a enemy on grid:

     11 12 13
    6 7 8 9 10
    1 2 3 4 5



    param: slot
        num 1-13

    return:
        None
    """
    loc = None
    if slot == 1:
        loc = (1034, 358)
    if slot == 2:
        loc = (1225, 454)
    if slot == 3:
        loc = (1433, 569)
    if slot == 4:
        loc = (1645, 677)
    if slot == 5:
        loc = (1854, 774)
    if slot == 6:
        loc = (1234, 255)
    if slot == 7:
        loc = (1431, 362)
    if slot == 8:
        loc = (1637, 460)
    if slot == 9:
        loc = (1834, 570)
    if slot == 10:
        loc = (2051, 675)
    if slot == 11:
        loc = (1660, 261)
    if slot == 12:
        loc = (1855, 361)
    if slot == 13:
        loc = (2031, 476)
    if return_coords:
        return loc
    else:
        precise_click(loc)
        return None


def click_drag(*args):
    if len(args) == 4:
        # 4 separate coordinates: start_x, start_y, end_x, end_y
        start_x, start_y, end_x, end_y = args
    elif len(args) == 2:
        # 2 tuples: (start_x, start_y), (end_x, end_y)
        (start_x, start_y), (end_x, end_y) = args
    else:
        raise ValueError("Pass either 4 coordinates or 2 tuples")

    pyautogui.moveTo(start_x, start_y, duration=0.1)
    pyautogui.mouseDown()
    pyautogui.moveTo(end_x, end_y, duration=0.2)
    pyautogui.mouseUp()


def check_win2():
    return look_for_image("victory.png")
