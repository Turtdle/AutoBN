import pyautogui
import big_foot_loop as bfl
import boar_badlands_loop as bbl
import navy_loop as nl
import time
import random
import utils
from utils import precise_click
import greenborough_loop as gl
import argparse

BOAR_BADLANDS = (1600, 700)
BIGFOOT_COUNTRY = (1833, 33)
GREENBOROUGH = (982, 1025)
OCEAN = (220, 1187)


def reset_world_map_zoom():
    pyautogui.moveTo(10, 1000)
    for i in range(150):
        pyautogui.scroll(-10, _pause=False)


def reset_world_map_zoom_left():
    pyautogui.moveTo(2400, 1000)
    for i in range(150):
        pyautogui.scroll(-10, _pause=False)


def look_for_go_button_world_map():
    """
    Looks for go button that appears after pressing a location on the world map
    Args:
        None
    Returns:
        Pixel location or None
    """
    try:
        location = pyautogui.locateOnScreen(
            "./images/go_world_map.png", grayscale=True, confidence=0.8
        )
        if location:
            print(f"Found at: {location}")
            return location
    except pyautogui.ImageNotFoundException:
        print("Image not found on screen")
        return None


def go_to_world_map(place: list, left=False):
    """
    Goes to a place from the world map; world map can be in any state
    Args:
        place: tuple of pixel value on map (x,y)
    Returns:
        None
    """
    if not left:
        reset_world_map_zoom()
    else:
        reset_world_map_zoom_left()
    time.sleep(0.5)
    precise_click(place)
    time.sleep(1)
    for i in range(20):
        a = look_for_go_button_world_map()
        if a:
            b = pyautogui.center(a)
            precise_click(b)
            break
    else:
        print(f"!!!ERROR IN GO TO {place}")


def main_loop(greenborough_count, navy_loop):
    if greenborough_count > 0:
        go_to_world_map(GREENBOROUGH)
        gl.greenborough_loop(greenborough_count)

    time.sleep(1)
    while True:
        if utils.check_for_stop():
            utils.remove_stop()
            break
        if not utils.retry_until(
            lambda: go_to_world_map(BOAR_BADLANDS), utils.wait_for_atk_button
        ):
            print("ERROR IN LOOKING FOR ATK BUTTON IN BOAR BADLANDS")

        bbl.boar_badlands_loop()

        def simple_delay():
            time.sleep(2)
            return utils.look_for_image("pfp.png")

        if navy_loop == 1:
            pyautogui.moveTo(2400, 600)
            for i in range(5):
                utils.scroll_down_fast()
            if not utils.retry_until(
                lambda: go_to_world_map(OCEAN, True), simple_delay
            ):
                print("ERROR IN LOOKING FOR ATK BUTTON IN BOAR BADLANDS")

            nl.navy_loop()
        if not utils.retry_until(
            lambda: go_to_world_map(BIGFOOT_COUNTRY), utils.wait_for_atk_button
        ):
            print("ERROR IN LOOKING FOR ATK BUTTON IN BOAR BADLANDS")
        bfl.big_foot_loop()
        time.sleep(2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Game automation script")
    parser.add_argument(
        "--greenborough-count",
        type=int,
        default=0,
        help="Number of greenborough loops to run (default: 30)",
    )
    parser.add_argument(
        "--navy-loop",
        type=int,
        default=0,
        help="Navy-loop?",
    )

    args = parser.parse_args()

    # start from world map
    time.sleep(2)
    main_loop(args.greenborough_count, args.navy_loop)
