import utils
import time
import pyautogui


def train_wimp():
    pyautogui.moveTo(870, 780)
    for i in range(10):
        pyautogui.scroll(-5)
    utils.precise_click(850, 574)
    utils.precise_click(1816, 1091)
    utils.precise_click(1920, 300)


def click_wait(click):
    utils.precise_click(click)
    time.sleep(2)


def task_2(first_run):
    time.sleep(1)
    racks = [
        (1352, 283),
        (1388, 257),
        (1427, 249),
        (1468, 218),
        (1507, 200),
        (1544, 181),
        (1390, 314),
        (1432, 289),
        (1462, 271),
        (1508, 250),
    ]
    collection_bubbles = [
        (1358, 261),
        (1400, 215),
        (1440, 195),
        (1480, 180),
        (1520, 165),
        (1560, 150),
        (1400, 255),
        (1440, 240),
        (1480, 225),
        (1520, 210),
    ]

    if not first_run:
        for bubble in collection_bubbles:
            utils.precise_click(bubble)
            time.sleep(0.1)

    time.sleep(1)

    for rack in racks:
        utils.retry_until(
            lambda: click_wait(rack),
            lambda: utils.look_for_image("barracks_menu.png"),
        )

        train_wimp()
        time.sleep(1)


def task_1_part_1():
    """First part of task_1 before the 95 second delay"""
    utils.retry_until(
        click_wait((1966, 634)),
        lambda: utils.look_for_image("barracks_menu.png"),
    )

    train_wimp()
    time.sleep(1)
    utils.retry_until(
        click_wait((2000, 650)),
        lambda: utils.look_for_image("barracks_menu.png"),
    )

    train_wimp()


def task_1_part_2():
    """Second part of task_1 after the delay"""
    utils.precise_click(1966, 634)
    utils.precise_click(2000, 650)


def task_1():
    """Complete task_1 with full 95 second delay"""
    task_1_part_1()
    time.sleep(95)
    task_1_part_2()


def main():
    pyautogui.moveTo(2500, 10)
    for i in range(5):
        utils.scroll_down_fast()

    # Track when task_2 was last run
    last_task_2_time = time.time()
    task_2_interval = 400  # 6 minutes in seconds
    first_task_2_run = True

    task_2(first_run=first_task_2_run)
    first_task_2_run = False
    print("Starting automated task runner...")
    print("Task 1 will run continuously, Task 2 every 6 minutes")

    while True:
        current_time = time.time()

        # Check if 6 minutes have passed since last task_2
        if current_time - last_task_2_time >= task_2_interval:
            print("Time for task_2! Running optimized sequence...")

            # Run first part of task_1
            print("Running task_1 part 1...")
            task_1_part_1()

            # Start timer and run task_2
            task_2_start_time = time.time()
            print("Running task_2 during delay period...")
            task_2(first_run=first_task_2_run)

            task_2_duration = time.time() - task_2_start_time

            # Calculate remaining delay time
            remaining_delay = max(0, 95 - task_2_duration)
            print(
                f"Task_2 took {task_2_duration:.1f}s, waiting {remaining_delay:.1f}s more..."
            )

            if remaining_delay > 0:
                time.sleep(remaining_delay)

            # Complete task_1
            print("Completing task_1...")
            task_1_part_2()

            last_task_2_time = current_time
            print("Optimized sequence completed, resuming normal task_1...")
        else:
            # Run normal task_1
            print("Running task_1...")
            task_1()
            print("Task_1 completed, checking timer...")


if __name__ == "__main__":
    time.sleep(2)
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram stopped by user")
    except Exception as e:
        print(f"An error occurred: {e}")
