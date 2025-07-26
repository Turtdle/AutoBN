import pyautogui
import time
import random
import utils


def choose_units():
    # select soldiers
    utils.precise_click((2368, 1245))

    utils.precise_click((2360, 1146))

    # scroll to end
    pyautogui.moveTo(1172, 1357)
    for i in range(150):
        pyautogui.scroll(-10, _pause=False)
    a = utils.look_for_image("heavy_icon.png")

    for i in range(5):
        utils.precise_click(a)

    b = utils.look_for_image("lightning_dragoon_icon.png")

    utils.precise_click(b)


def wait_for_atk_button():
    hex_color = "73e609"
    target_rgb = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return pyautogui.pixel(2462, 1324) == target_rgb


def turn_loop():
    utils.retry_until(
        lambda: (
            utils.select_unit_slot(8),
            time.sleep(0.1),
            utils.click_generic_middle_enemy(),
        ),
        utils.check_turn,
        45,
    )

    while True:
        for i in range(1, 6):

            def _atk():
                time.sleep(0.5)
                utils.select_unit_slot(i)
                time.sleep(0.5)
                utils.click_generic_middle_enemy()

            _atk()
            while not utils.check_turn() and not utils.check_win():
                time.sleep(1)
            if utils.check_win():
                return


def boar_badlands_loop():
    # function assuming atk button is visible in map ui

    done = False
    done_inner = False
    while not done:
        while not done_inner:
            if utils.check_for_stop():
                break
            a = utils.look_for_image("boar_badlands_nose.png")
            if not a:
                done_inner = True
            else:
                if not utils.retry_until(
                    click_input=lambda: utils.precise_click(a),
                    y_or_check=utils.check_select,
                    retry_time=20,
                ):
                    print("ERROR IN WAITING FOR CHECK SELECT IN BB")

                choose_units()

                utils.retry_until(2365, 902, check_function=utils.check_turn)

                turn_loop()

                utils.battle_done()
                for k in range(20):
                    if wait_for_atk_button():
                        break
                    time.sleep(1)
        if utils.check_for_stop():
            break
        for i in range(1500):
            pyautogui.scroll(-10, _pause=False)
        time.sleep(1)
        c = utils.look_for_image("boar_badlands_nose.png")
        if not c:
            done = True
        else:
            if not utils.retry_until(
                click_input=lambda: utils.precise_click(a),
                y_or_check=utils.check_select,
                retry_time=20,
            ):
                print("ERROR IN WAITING FOR CHECK SELECT IN BB")

            choose_units()

            utils.retry_until(2365, 902, check_function=utils.check_turn)

            turn_loop()

            utils.retry_until(
                click_input=utils.battle_done, check_function=wait_for_atk_button
            )

    # return us safely to main map
    while True:
        if wait_for_atk_button():
            utils.retry_until((2094, 1336), lambda: utils.look_for_image("pfp.png"))
            break


if __name__ == "__main__":
    time.sleep(2)
    boar_badlands_loop()
