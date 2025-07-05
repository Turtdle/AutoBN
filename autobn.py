import pyautogui
import time
import numpy as np
from PIL import Image, ImageDraw
import random


def atk():
    pyautogui.click(2460, 1330)


def green_check():
    pyautogui.mouseDown(1268, 655)
    pyautogui.moveTo(1119, 372, 1.5)
    pyautogui.mouseUp(1268, 655)
    time.sleep(0.5)
    pyautogui.click(1268, 655)
    pyautogui.click(1182, 479)


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
    pyautogui.mouseDown(1128, 678)
    time.sleep(random.uniform(0.09, 0.11))
    pyautogui.mouseUp(1128, 678)


def select_heavy_4():
    pyautogui.mouseDown(1338, 786)
    time.sleep(random.uniform(0.09, 0.11))
    pyautogui.mouseUp(1338, 786)


def select_heavy_5():
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


class DiamondGrid:
    def __init__(self):
        # Base diamond coordinates (top-left cell)
        self.base_diamond = {
            "top": (1022, 265),
            "right": (1228, 368),
            "bottom": (1021, 472),
            "left": (814, 368),
        }

        self.base_center_x = (
            self.base_diamond["left"][0] + self.base_diamond["right"][0]
        ) // 2
        self.base_center_y = (
            self.base_diamond["top"][1] + self.base_diamond["bottom"][1]
        ) // 2

        self.horizontal_step = 207
        self.vertical_step = 103.5

        # Grid dimensions
        self.grid_rows = 6
        self.grid_cols = 8

    def get_diamond_center(self, row, col):
        """Get the center point of a diamond at grid position (row, col)."""
        center_x = (
            self.base_center_x
            + (col * self.horizontal_step)
            + (row * -self.horizontal_step)
        )
        center_y = (
            self.base_center_y + (col * self.vertical_step) + (row * self.vertical_step)
        )
        return (int(center_x), int(center_y))

    def get_diamond_vertices(self, row, col):
        """Get all four vertices of a diamond at grid position (row, col)."""
        center_x, center_y = self.get_diamond_center(row, col)

        # Calculate vertices relative to center
        # Using the original diamond as reference
        top = (center_x + 1, center_y - 103)  # Slightly right, up
        right = (center_x + 207, center_y)  # Right
        bottom = (center_x, center_y + 104)  # Down
        left = (center_x - 207, center_y)  # Left

        return {"top": top, "right": right, "bottom": bottom, "left": left}

    def get_diamond_bounding_box(self, row, col):
        """Get rectangular bounding box containing the diamond."""
        vertices = self.get_diamond_vertices(row, col)

        min_x = min(v[0] for v in vertices.values())
        max_x = max(v[0] for v in vertices.values())
        min_y = min(v[1] for v in vertices.values())
        max_y = max(v[1] for v in vertices.values())

        return (min_x, min_y, max_x, max_y)

    def point_in_diamond(self, x, y, row, col):
        """Check if a point (x,y) is inside the diamond at (row,col)."""
        vertices = self.get_diamond_vertices(row, col)

        # Use the point-in-polygon algorithm for the diamond
        def point_in_polygon(x, y, vertices_list):
            n = len(vertices_list)
            inside = False

            j = n - 1
            for i in range(n):
                xi, yi = vertices_list[i]
                xj, yj = vertices_list[j]

                if ((yi > y) != (yj > y)) and (
                    x < (xj - xi) * (y - yi) / (yj - yi) + xi
                ):
                    inside = not inside
                j = i

            return inside

        vertices_list = [
            vertices["top"],
            vertices["right"],
            vertices["bottom"],
            vertices["left"],
        ]
        return point_in_polygon(x, y, vertices_list)


def detect_boars_in_diamond_grid(screenshot_path=None, debug=False):
    """
    Detect boars in the diamond grid using proper diamond-shaped regions.
    Only checks squares 0,0 to 0,5.
    """
    grid = DiamondGrid()

    # Capture or load screenshot
    if screenshot_path:
        screenshot = Image.open(screenshot_path)
    else:
        screenshot = pyautogui.screenshot()

    img_array = np.array(screenshot)
    boar_positions = []

    # Boar color detection (pink/flesh tones)
    boar_color_lower = np.array([180, 120, 120])
    boar_color_upper = np.array([255, 180, 160])

    # Only check row 0, columns 0 to 5
    for col in range(6):  # 0 to 5 (6 total)
        row = 0
    # Only check row 0, columns 0 to 5
    for col in range(6):  # 0 to 5 (6 total)
        row = 0

        # Get diamond bounding box for initial crop
        min_x, min_y, max_x, max_y = grid.get_diamond_bounding_box(row, col)

        # Make sure bounds are within image
        if (
            min_x < 0
            or min_y < 0
            or max_x >= img_array.shape[1]
            or max_y >= img_array.shape[0]
        ):
            continue

        # Count boar pixels only within the actual diamond shape
        boar_pixels = 0

        for y in range(max(0, min_y), min(img_array.shape[0], max_y)):
            for x in range(max(0, min_x), min(img_array.shape[1], max_x)):
                # Check if this pixel is inside the diamond
                if grid.point_in_diamond(x, y, row, col):
                    pixel = img_array[y, x]
                    # Check if pixel matches boar color
                    if (
                        boar_color_lower[0] <= pixel[0] <= boar_color_upper[0]
                        and boar_color_lower[1] <= pixel[1] <= boar_color_upper[1]
                        and boar_color_lower[2] <= pixel[2] <= boar_color_upper[2]
                    ):
                        boar_pixels += 1

        # Threshold for boar detection
        boar_threshold = 50  # Adjust as needed

        if boar_pixels > boar_threshold:
            boar_positions.append((row, col))
            center_x, center_y = grid.get_diamond_center(row, col)

            if debug:
                print(
                    f"Boar detected at grid ({row},{col}) with {boar_pixels} boar-colored pixels"
                )
                print(f"  Diamond center: ({center_x},{center_y})")

    return boar_positions, grid


def visualize_diamond_grid(
    screenshot_path=None, output_path="diamond_grid_overlay.png"
):
    """
    Create a visualization showing the diamond grid overlay on the screenshot.
    Only creates squares 0,0 to 0,5.
    """
    grid = DiamondGrid()

    if screenshot_path:
        screenshot = Image.open(screenshot_path)
    else:
        screenshot = pyautogui.screenshot()

    # Create overlay
    overlay = screenshot.copy()
    draw = ImageDraw.Draw(overlay)

    # Draw only row 0, columns 0 to 5
    for col in range(6):  # 0 to 5 (6 total)
        row = 0
        vertices = grid.get_diamond_vertices(row, col)

        # Create list of vertices for drawing
        diamond_points = [
            vertices["top"],
            vertices["right"],
            vertices["bottom"],
            vertices["left"],
        ]

        # Draw diamond outline
        draw.polygon(diamond_points, outline="red", width=2)

        # Draw grid coordinates at center
        center_x, center_y = grid.get_diamond_center(row, col)
        draw.text((center_x - 10, center_y - 5), f"{row},{col}", fill="yellow")

    overlay.save(output_path)
    print(f"Diamond grid overlay saved as {output_path}")
    print("Showing only squares (0,0) to (0,5)")


def click_the_boar(target, grid):
    time.sleep(1)
    pyautogui.mouseDown(grid.get_diamond_center(target[0], target[1]))
    time.sleep(0.5)
    pyautogui.mouseUp(grid.get_diamond_center(target[0], target[1]))
    time.sleep(1)
    pyautogui.mouseDown(grid.get_diamond_center(target[0], target[1]))
    time.sleep(0.5)
    pyautogui.mouseUp(grid.get_diamond_center(target[0], target[1]))


def check_winbad(
    top_left_x=1049,
    top_left_y=784,
    bottom_right_x=1071,
    bottom_right_y=819,
    target_color=(165, 161, 149),
):
    width = bottom_right_x - top_left_x
    height = bottom_right_y - top_left_y

    screenshot = pyautogui.screenshot(region=(top_left_x, top_left_y, width, height))

    if screenshot.mode != "RGB":
        screenshot = screenshot.convert("RGB")

    pixels = list(screenshot.getdata())
    print(f"win: {all(pixel == target_color for pixel in pixels)}")
    return all(pixel == target_color for pixel in pixels)


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


def turn_loop():

    while not check_turn():
        time.sleep(0.1)
    select_wimp()
    select_wimp()
    time.sleep(0.3)
    pyautogui.mouseDown(1426, 553)
    time.sleep(random.uniform(0.09, 0.11))
    pyautogui.mouseUp(1426, 553)
    while not check_turn():
        time.sleep(0.1)
    select_saboteur()
    select_saboteur()
    pyautogui.mouseDown(850, 1350)
    time.sleep(random.uniform(0.09, 0.11))
    pyautogui.mouseUp(850, 1350)
    time.sleep(0.1)
    pyautogui.mouseDown(1650, 450)
    time.sleep(random.uniform(0.09, 0.11))
    pyautogui.mouseUp(1650, 450)

    time.sleep(1)

    heavy_num = 0
    while True:
        heavy_select_funcs = [
            select_heavy_1,
            select_heavy_2,
            select_heavy_3,
            select_heavy_4,
            select_heavy_5,
        ]
        if check_turn():
            time.sleep(random.uniform(1, 2))
            heavy_select_funcs[heavy_num]()
            pyautogui.mouseDown(1426, 553)
            time.sleep(random.uniform(0.09, 0.11))
            pyautogui.mouseUp(1426, 553)
            heavy_num += 1
            if heavy_num == 5:
                heavy_num = 0
        if check_win():
            break


def scroll_right():
    pyautogui.moveTo(1400, 1356)
    for i in range(11):
        pyautogui.scroll(3)
        time.sleep(0.001)

    time.sleep(1)
    for i in range(5):
        pyautogui.click(250, 1360)
    for i in range(19):
        pyautogui.scroll(-3)
        time.sleep(0.0001)

    pyautogui.click(1725, 1352)  # bike

    for i in range(3):
        pyautogui.moveTo(60, 1350, 0.3)
        pyautogui.dragTo(2400, 900, 0.3, button="left")

    pyautogui.click(800, 1352)  # PK
    time.sleep(0.2)
    for i in range(4):
        pyautogui.moveTo(2400, 1350, 0.2)
        pyautogui.dragTo(100, 900, 0.2, button="left")
    time.sleep(1)


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


def check_select():
    hex_color = "ffffff"
    target_rgb = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return pyautogui.pixel(2422, 900) == target_rgb


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


if __name__ == "__main__":
    counter = 0
    time.sleep(1)

    while True:
        if wait_for_atk_button():
            print(f"Times run: {counter}")
            atk()
            time.sleep(random.uniform(0.9, 1.5))
            green_check()
            done = False
            while not done:
                w = 0
                try_again = False
                while not try_again:
                    if check_select():
                        done = True
                        break
                    time.sleep(1.5)
                    w += 1
                    if w >= 10:
                        try_again = True
                green_check()

            time.sleep(random.uniform(1, 3))

            scroll_right()

            fight()
            turn_loop()
            time.sleep(0.5)
            pyautogui.click(1570, 1031)
            pyautogui.screenshot("shared_folder/screenshot.png")
            time.sleep(0.5)
            pyautogui.click(1570, 1031)
            counter += 1
            if check_for_stop():
                break
