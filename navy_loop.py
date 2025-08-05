import utils
import time
import pyautogui
import numpy as np


def choose_units():
    a = utils.look_for_image("you_may_only_place.png")
    units_placed = 0
    while not a:
        units_placed += 1
        utils.precise_click((1125, 1350))
        time.sleep(0.1)
        a = utils.look_for_image("you_may_only_place.png")
    units_placed -= 1
    utils.precise_click((1125, 1350))
    return units_placed


def calculate_m10(number_deployed, last_used):
    if last_used == number_deployed:
        if number_deployed == 4:
            return 2, True
        return 1, True
    if last_used < 5:
        if number_deployed == 4:
            return last_used + 3, False
        return last_used + 1, False
    if last_used == 5:
        return 8, False
    if last_used == 6:
        return 9, False
    if last_used == 7:
        return 7, False
    else:
        raise ValueError


def turn_loop(m10s):
    # first turn, before m10s move forward
    while not utils.check_turn():
        time.sleep(0.1)
    enemy = find_enemies(in_battle=True)
    time.sleep(1)
    if m10s == 4:
        utils.select_unit_slot(7)
    else:
        utils.select_unit_slot(6)
    time.sleep(0.1)
    utils.select_ability(2)

    utils.click_drag(utils.select_enemy_slot(8, True), utils.select_enemy_slot(3, True))
    time.sleep(1)
    utils.click_drag(
        utils.select_enemy_slot(3, True), utils.select_enemy_slot(enemy, True)
    )
    time.sleep(0.1)
    utils.click_generic_middle_enemy()

    last_used = 1
    while not utils.check_win():
        print(f"last used: {last_used}")
        while not utils.check_turn() and not utils.check_win2():
            time.sleep(0.1)
        if utils.check_win2():
            continue
        time.sleep(1)
        x = calculate_m10(last_used=last_used, number_deployed=m10s)
        enemy = find_enemies(in_battle=True)
        utils.select_unit_slot(x[0])
        time.sleep(0.1)
        utils.select_ability(2)

        utils.click_drag(
            utils.select_enemy_slot(8, True), utils.select_enemy_slot(3, True)
        )

        time.sleep(1)

        utils.click_drag(
            utils.select_enemy_slot(3, True), utils.select_enemy_slot(enemy, True)
        )
        time.sleep(0.1)
        utils.click_generic_middle_enemy()
        if x[1]:
            last_used = 1
        else:
            last_used += 1


def find_enemies(in_battle=False, debug=True):
    if in_battle:
        for i in range(5):
            pyautogui.click(2453, 1229)
    diamond_images = []
    marked_positions = set()
    for i, coords in enumerate(utils.DIAMOND_COORDS):
        diamond_img = utils.diamond_screenshot(
            **{
                f"{pos}_{axis}": coords[pos][0 if axis == "x" else 1]
                for pos in ["top", "left", "right", "bottom"]
                for axis in ["x", "y"]
            }
        )
        diamond_images.append(diamond_img)
        avg_color = utils.calculate_diamond_average_color(diamond_img, coords)
        if debug:
            print(f"i: {i}, {avg_color}")
        if (
            (
                ((avg_color[0] > 26 or avg_color[2] < 118) and avg_color[2] < 150)
                or (avg_color[0] > 30 and avg_color[1] < 120 and avg_color[2] < 160)
                or is_within_cumulative_error(
                    avg_color, [24.12837367, 114.5045292, 152.0923956], 15
                )
            )
            and not is_within_cumulative_error(
                avg_color, [25.52301761, 120.63299577, 158.20207182], 5
            )
            and not is_within_cumulative_error(
                avg_color, [23.25742091, 116.05191155, 144.33469596], 5
            )
            and not is_within_cumulative_error(
                avg_color, [27.32415107, 103.63531844, 132.34965392], 5
            )
            and not is_within_cumulative_error(
                avg_color, [21.79360803, 114.42641799, 141.41564082], 5
            )
            and not is_within_cumulative_error(
                avg_color, [29.64370326, 127.43498862, 149.52517768], 5
            )
            and not is_within_cumulative_error(
                avg_color, [33.78441028, 123.95366284, 146.34027036], 5
            )
            and not is_within_cumulative_error(
                avg_color, [21.66783574, 121.51368049, 150.20365123], 5
            )
        ):
            marked_positions.add(i)
    pattern = [
        [10, 11, 12],
        [5, 6, 7, 8, 9],
        [0, 1, 2, 3, 4],
    ]
    print("Diamond Pattern:")
    for row in pattern:
        if len(row) == 3:
            line = (
                " "
                + "".join("x" if pos in marked_positions else "o" for pos in row)
                + " "
            )
        elif len(row) == 5:
            line = "".join("x" if pos in marked_positions else "o" for pos in row)
        print(line)

    triangle_patterns = {
        # Bottom row attacks hit middle row + self
        0: [0, 6],  # Attack from 0 hits 0 and 6
        1: [1, 5, 7],  # Attack from 1 hits 1, 5, and 7
        2: [2, 6, 8],  # Attack from 2 hits 2, 6, and 8
        3: [3, 7, 9],  # Attack from 3 hits 3, 7, and 9
        4: [4, 8],  # Attack from 4 hits 4 and 8
        # Middle row attacks hit top row + self
        5: [5, 10],  # Attack from 5 hits 5 and 10
        6: [6, 11],  # Attack from 6 hits 6 and 11
        7: [7, 10, 12],  # Attack from 7 hits 7, 10, and 12
        8: [8, 11],  # Attack from 8 hits 8 and 11
        9: [9, 12],  # Attack from 9 hits 9 and 12
    }

    best_attack_pos = None
    max_hits = 0

    for attack_pos, hit_positions in triangle_patterns.items():
        hits = sum(1 for pos in hit_positions if pos in marked_positions)
        print(f"Position {attack_pos}: hits {hit_positions} → {hits} hits")
        if hits > max_hits:
            max_hits = hits
            best_attack_pos = attack_pos
            print(f"New best: position {attack_pos} with {hits} hits")

    # If no triangle attack hits enemies, just attack the first enemy found
    if best_attack_pos is None and marked_positions:
        best_attack_pos = min(marked_positions)
    if in_battle:
        for i in range(5):
            pyautogui.click(2451, 1023)

    if best_attack_pos is not None:
        # print(f"TRYING TO HIT {best_attack_pos + 1}")
        return best_attack_pos + 1
    return None


def find_target():
    pyautogui.moveTo(2390, 637)
    for i in range(5):
        utils.scroll_down_fast()
    for i in range(6):
        a = utils.look_for_image(f"navy{i + 1}.png", _confidence=0.7)
        if a:
            return a
    pyautogui.moveTo(100, 637)
    for i in range(5):
        utils.scroll_down_fast()
    for i in range(6):
        a = utils.look_for_image(f"navy{i + 1}.png", _confidence=0.7)
        if a:
            return a
    print("uhoh")
    return None


def navy_loop():
    utils.look_for_image_with_wait("pfp2.png")
    time.sleep(2)
    a = find_target()
    time.sleep(5)
    while a:
        if utils.check_for_stop():
            break

        else:
            if not utils.retry_until(
                click_input=lambda: utils.precise_click(a),
                y_or_check=utils.check_select,
                retry_time=20,
            ):
                print("ERROR IN WAITING FOR CHECK SELECT IN NAVY")
        m10s = choose_units()
        utils.retry_until(2365, 902, check_function=utils.check_turn)
        turn_loop(m10s)
        time.sleep(0.1)

        utils.retry_until(
            lambda: utils.battle_done(), lambda: utils.look_for_image("pfp.png")
        )
        a = find_target()
        if not a:
            break
    # return us safely to main map
    while True:
        a = utils.look_for_image("pfp.png")
        if a:
            pyautogui.click(2445, 1337)
            break
    time.sleep(1)
    while True:
        a = utils.look_for_image("pfp.png")
        if a:
            pyautogui.click(2445, 1337)
            break


def is_within_cumulative_error(reference, test_array, max_error):
    reference = np.array(reference)
    test_array = np.array(test_array)

    # Calculate absolute differences
    differences = np.abs(reference - test_array)

    # Sum up all the errors (cumulative)
    cumulative_error = np.sum(differences)

    return cumulative_error <= max_error


if __name__ == "__main__":
    # navy_loop()
    find_enemies(True, True)
