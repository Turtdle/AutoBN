import pyautogui
import time
import random
import utils


def greenborough_loop(amount_of_iron=60):
    for i in range(amount_of_iron // 30):
        print(f"gl run: {i} out of {amount_of_iron // 30}")
        for _i in range(20):
            if utils.wait_for_atk_button():
                break
            time.sleep(1)
        else:
            print("REIHJAERIARHEUJHERUOAHEUOJERUAHOHAEOJNHEROAJOJN GERENBOUGHIOGU")

        pyautogui.moveTo(2488, 694)
        utils.scroll_down_fast()
        utils.scroll_down_fast()
        utils.scroll_down_fast()
        time.sleep(1)
        utils.precise_click((2460, 1330))

        pyautogui.mouseDown(1270, 684)
        pyautogui.moveTo(1419, 561, 0.5)
        pyautogui.mouseUp(1419, 561)

        utils.precise_click((1483, 647))

        for _i in range(20):
            if utils.check_select():
                break
            time.sleep(1)
        else:
            print("ERROR WAITING FOR CHECK SELECT IN GROUBOUGGOU")

        pyautogui.moveTo(1557, 1342)

        utils.scroll_up_fast()

        g = utils.look_for_image("salamander_icon.png")
        for _i in range(3):
            pyautogui.mouseDown(g)
            time.sleep(random.uniform(0.009, 0.011))
            pyautogui.mouseUp(g)

        utils.precise_click((2365, 902))
        s = 0
        while True:
            s += 1
            utils.select_unit_slot((s % 3) + 2)
            time.sleep(0.1)
            # select third ability (should add to utils later)
            utils.precise_click((942, 1330))

            utils.click_all_front_row()
            if utils.check_win():
                break
            time.sleep(0.5)
        utils.battle_done(screenshot=False)

    while True:
        if utils.wait_for_atk_button():
            utils.precise_click((2094, 1336))
            break
        time.sleep(0.1)


if __name__ == "__main__":
    time.sleep(2)
    greenborough_loop()
