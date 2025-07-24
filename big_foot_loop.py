import pyautogui
import time
import random
import utils
from utils import check_win, check_turn, battle_done, check_select


def atk():
    pyautogui.click(2460, 1330)


def green_check():
    pyautogui.click(1332, 777)


def baby_raptor():
    pyautogui.click(1702, 1350)


def wimp():
    pyautogui.click(2285, 1351)


def trooper():
    pyautogui.click(2285, 1352)


def fight():
    pyautogui.click(2380, 900)


def select_heavy_1():
    pyautogui.mouseDown(711, 486)
    time.sleep(random.uniform(0.09, 0.11))
    pyautogui.mouseUp(711, 486)


def select_heavy_2():
    pyautogui.mouseDown(951, 570)
    time.sleep(random.uniform(0.09, 0.11))
    pyautogui.mouseUp(951, 570)


def select_heavy_3():
    pyautogui.mouseDown(1338, 786)
    time.sleep(random.uniform(0.09, 0.11))
    pyautogui.mouseUp(1338, 786)


def select_heavy_4():
    pyautogui.mouseDown(1548, 906)
    time.sleep(random.uniform(0.09, 0.11))
    pyautogui.mouseUp(1548, 906)


def select_wimp():
    pyautogui.mouseDown(900, 800)
    time.sleep(random.uniform(0.09, 0.11))
    pyautogui.mouseUp(900, 800)


def heavy():
    pyautogui.click(2518, 1350)


def select_saboteur():
    pyautogui.mouseDown(1200, 900)
    time.sleep(random.uniform(0.09, 0.11))
    pyautogui.mouseUp(1200, 900)


def select_field_agent():
    pyautogui.mouseDown(1400, 1400)
    time.sleep(random.uniform(0.09, 0.11))
    pyautogui.mouseUp(1400, 1400)


def click_all_front_row():
    pyautogui.mouseDown(1000, 350)
    time.sleep(random.uniform(0.09, 0.11))
    pyautogui.mouseUp(1000, 350)
    time.sleep(0.005)

    pyautogui.mouseDown(1200, 450)
    time.sleep(random.uniform(0.09, 0.11))
    pyautogui.mouseUp(1200, 450)
    time.sleep(0.005)

    pyautogui.mouseDown(1400, 575)
    time.sleep(random.uniform(0.09, 0.11))
    pyautogui.mouseUp(1400, 575)
    time.sleep(0.005)
    #
    pyautogui.mouseDown(1650, 650)
    time.sleep(random.uniform(0.09, 0.11))
    pyautogui.mouseUp(1650, 650)
    time.sleep(0.005)

    pyautogui.mouseDown(1850, 750)
    time.sleep(random.uniform(0.09, 0.11))
    pyautogui.mouseUp(1850, 750)
    time.sleep(0.005)


def turn_loop():
    while not check_turn():
        time.sleep(0.1)

    # bask
    pyautogui.mouseDown(900, 820)
    time.sleep(random.uniform(0.09, 0.11))
    pyautogui.mouseUp(900, 820)
    pyautogui.mouseDown(900, 820)
    time.sleep(random.uniform(0.09, 0.11))
    pyautogui.mouseUp(900, 820)

    click_all_front_row()

    while not check_turn():
        time.sleep(0.1)

    # select heavy chem
    pyautogui.mouseDown(1111, 750)
    time.sleep(random.uniform(0.09, 0.11))
    pyautogui.mouseUp(1111, 750)
    pyautogui.mouseDown(1111, 750)
    time.sleep(random.uniform(0.09, 0.11))
    pyautogui.mouseUp(1111, 750)

    # press enemy
    time.sleep(0.3)
    pyautogui.mouseDown(1426, 553)
    time.sleep(random.uniform(0.09, 0.11))
    pyautogui.mouseUp(1426, 553)

    time.sleep(1)

    while not check_turn():
        time.sleep(0.1)

    heavy_num = 0
    while True:
        time.sleep(1)
        print(pyautogui.pixel(903, 525))
        heavy_select_funcs = [
            select_heavy_1,
            select_heavy_2,
            select_heavy_3,
            select_heavy_4,
        ]
        while not check_turn() and not check_win():
            time.sleep(1)
        time.sleep(1)
        heavy_select_funcs[heavy_num]()
        click_all_front_row()
        heavy_num += 1
        if heavy_num == 4:
            heavy_num = 0
        if check_win():
            break


def scroll_right():
    for i in range(150):
        pyautogui.scroll(-10, _pause=False)
    time.sleep(0.3)
    pyautogui.click(1450, 1350)
    time.sleep(0.2)
    for i in range(4):
        pyautogui.click(2300, 1350)
    pyautogui.click(1300, 1350)
    pyautogui.click(1600, 1350)


def move_top_wimp():
    pyautogui.mouseDown(718, 484)
    pyautogui.moveTo(718, 739, 1)
    pyautogui.mouseUp(718, 739)


def select_bottom_wimp():
    pyautogui.mouseDown(1555, 892)
    time.sleep(random.uniform(0.09, 0.11))
    pyautogui.mouseUp(1555, 892)


def move_bottom_wimp():
    pyautogui.mouseDown(1555, 892)
    pyautogui.moveTo(1092, 933, 1)
    pyautogui.mouseUp(1092, 933)


def wait_for_atk_button():
    hex_color = "73e609"
    target_rgb = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return pyautogui.pixel(2462, 1324) == target_rgb


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
            os.remove(stop_file_path)
            print("Stop signal detected - stop.txt found and removed")
            return True
        except Exception as e:
            print(f"Error removing stop.txt: {e}")
            return True  # Still signal to stop even if we can't delete

    return False


def big_foot_loop():
    counter = 0
    time.sleep(1)
    start_time = time.time()
    duration = 1 * 60  # 20 minutes in seconds

    while time.time() - start_time < duration:
        if wait_for_atk_button():
            print(f"Times run: {counter}")
            atk()
            time.sleep(random.uniform(0.9, 1.5))
            green_check()

            while not check_select():
                time.sleep(1)

            time.sleep(random.uniform(1, 3))

            scroll_right()

            fight()
            turn_loop()
            battle_done()
            counter += 1
            if check_for_stop():
                break
    while True:
        if wait_for_atk_button():
            utils.precise_click((2094, 1336))
            break
        time.sleep(0.1)
