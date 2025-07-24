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
    for i in range(20):
        if utils.check_turn():
            break
        time.sleep(1)

    utils.select_unit_slot(8)
    time.sleep(0.1)
    utils.click_generic_middle_enemy()

    print("starting heavy loop")
    while True:
        for i in range(1, 6):
            print(i)
            for j in range(20):
                print(f"waiting for check turn: {j}")
                if utils.check_turn():
                    break
                if utils.check_win():
                    return
                time.sleep(1)
            else:
                print("ERROR IN WAITING FOR TURN TO COME IN BOAR LOOP")
            time.sleep(0.5)
            print("atking")
            utils.select_unit_slot(i)
            print(f"tried to select unit: {i}")
            time.sleep(0.5)
            utils.click_generic_middle_enemy()


def boar_badlands_loop():
    for i in range(20):
        if wait_for_atk_button():
            break
        time.sleep(1)
    else:
        print("ERROR IN LOOKING FOR ATK BUTTON IN BOAR BADLANDS")
    print("found atk button")
    done = False
    while not done:
        done_inner = False
        while not done_inner:
            a = utils.look_for_image("boar_badlands_nose.png")
            if not a:
                done_inner = True
            else:
                print(f"clicking: {a}")
                utils.precise_click(a)

                for i in range(20):
                    if utils.check_select():
                        break
                    time.sleep(1)
                else:
                    print("ERROR IN WAITING FOR CHECK SELECT IN BB")

                choose_units()

                # press fight button
                utils.precise_click((2365, 902))

                turn_loop()

                utils.battle_done()
                for k in range(20):
                    if wait_for_atk_button():
                        break
                    time.sleep(1)
        for i in range(1500):
            pyautogui.scroll(-10, _pause=False)
        time.sleep(1)
        c = utils.look_for_image("boar_badlands_nose.png")
        if not c:
            done = True
        else:
            print(f"clicking: {c}")
            utils.precise_click(c)

            for i in range(20):
                if utils.check_select():
                    break
                time.sleep(1)
            else:
                print("ERROR IN WAITING FOR CHECK SELECT IN BB")

            choose_units()

            # press fight button
            utils.precise_click((2365, 902))

            turn_loop()

            utils.battle_done()
            for k in range(20):
                if wait_for_atk_button():
                    break
                time.sleep(1)
    while True:
        if wait_for_atk_button():
            utils.precise_click((2094, 1336))
            break
        time.sleep(0.1)
