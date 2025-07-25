import pyautogui
import time
import random
from typing import Callable, Union, Tuple


def precise_click(location):
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


def click_generic_middle_enemy():
    precise_click((1400, 575))


def select_unit_slot(slot: int):
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
    precise_click(loc)


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
