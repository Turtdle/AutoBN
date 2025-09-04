import pyautogui
import time
import random
import utils
from utils import check_win, check_turn, battle_done, check_select, check_for_stop


def atk():
    utils.precise_click((2460, 1330))
    time.sleep(random.uniform(0.9, 1.5))
    utils.precise_click((1332, 777))


def baby_raptor():
    pyautogui.click(1702, 1350)


def wimp():
    pyautogui.click(2285, 1351)


def trooper():
    pyautogui.click(2285, 1352)


def fight():
    pyautogui.click(2380, 900)
    time.sleep(0.1)
    pyautogui.click(2380, 900)
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
    time.sleep(0.005)


def turn_loop():
    while not check_turn():
        time.sleep(0.1)
    time.sleep(1)
    utils.select_unit_slot(8)
    click_all_front_row()
    utils.retry_until(
        lambda: (time.sleep(0.1)),
        utils.check_turn,
        45,
    )

    utils.retry_until(
        lambda: (
            utils.select_unit_slot(9),
            time.sleep(0.1),
            click_all_front_row(),
        ),
        utils.check_turn,
        45,
    )

    time.sleep(1)

    while True:
        for i in range(1, 6):

            def _atk():
                time.sleep(0.5)
                utils.select_unit_slot(i)
                time.sleep(0.5)
                click_all_front_row()

            _atk()
            while not utils.check_turn() and not utils.check_win():
                time.sleep(1)
            if utils.check_win():
                return


def scroll_right():
    pyautogui.moveTo(1450, 1350)
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


def choose_units():
    # press vehicles
    utils.precise_click((2343, 1243))
    time.sleep(0.1)
    utils.precise_click((2345, 1053))

    # scroll to end

    pyautogui.moveTo(1172, 1357)
    for i in range(500):
        pyautogui.scroll(-10, _pause=False)

    time.sleep(1)

    for i in range(20):
        b = utils.look_for_image("super_tank_icon.png")
        if not b:
            time.sleep(1)
        else:
            break
    time.sleep(0.1)

    time.sleep(0.1)
    for _i in range(5):
        utils.precise_click(b)
    utils.precise_click(2024, 1350)
    time.sleep(0.1)
    utils.scroll_up_fast()

    time.sleep(0.1)
    utils.precise_click((2343, 1243))
    time.sleep(0.1)
    utils.precise_click((2345, 950))

    pyautogui.moveTo(1172, 1357)
    for i in range(500):
        pyautogui.scroll(10, _pause=False)
    time.sleep(1.1)
    utils.precise_click((410, 1350))
    time.sleep(0.1)


def big_foot_loop(duration=45):
    counter = 0
    time.sleep(1)
    start_time = time.time()
    duration = duration * 60  # 20 minutes in seconds

    while time.time() - start_time < duration:
        if wait_for_atk_button():
            print(f"Times run: {counter}")
            atk()
            while not check_select():
                time.sleep(1)
            # utils.retry_until(atk, check_select, 60)

            time.sleep(random.uniform(1, 3))

            choose_units()

            fight()
            turn_loop()
            battle_done()
            counter += 1
            if check_for_stop():
                break

    while True:
        if wait_for_atk_button():
            utils.retry_until((2094, 1336), lambda: utils.look_for_image("pfp.png"))
            break


if __name__ == "__main__":
    choose_units()
    # big_foot_loop(duration=1)
