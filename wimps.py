import utils
import time
import pyautogui

if __name__ == "__main__":
    time.sleep(1)
    while True:
        utils.precise_click(1966, 634)
        time.sleep(2)
        pyautogui.moveTo(870, 780)
        for i in range(10):
            pyautogui.scroll(-5)
        utils.precise_click(850, 574)
        utils.precise_click(1816, 1091)
        utils.precise_click(1920, 300)
        time.sleep(1)
        utils.precise_click(2000, 650)
        time.sleep(2)
        pyautogui.moveTo(870, 780)
        for i in range(10):
            pyautogui.scroll(-5)
        utils.precise_click(850, 574)
        utils.precise_click(1816, 1091)
        utils.precise_click(1920, 300)
        time.sleep(95)

        utils.precise_click(1966, 634)
        utils.precise_click(2000, 650)
