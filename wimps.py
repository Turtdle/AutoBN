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


def task_2(first_run):
    racks = [
        (1352, 283),
        (1388, 257),
        (1427, 249),
        (1468, 218),
        (1507, 200),
        (1544, 181),
        (1390, 314),
        (1432, 289),
    ]
    if not first_run:
        for rack in racks:
            utils.precise_click(rack)
            time.sleep(0.1)
    time.sleep(1)
    for rack in racks:
        utils.precise_click(rack)
        time.sleep(2)
        train_wimp()
        time.sleep(1)


def task_1():
    utils.precise_click(1966, 634)
    time.sleep(2)
    train_wimp()
    time.sleep(1)
    utils.precise_click(2000, 650)
    time.sleep(2)
    train_wimp()
    time.sleep(95)
    utils.precise_click(1966, 634)
    utils.precise_click(2000, 650)


def main():
    # Track when task_2 was last run
    last_task_2_time = time.time()
    task_2_interval = 400  # 6 minutes in seconds
    first_task_2_run = True

    print("Starting automated task runner...")
    print("Task 1 will run continuously, Task 2 every 6 minutes")

    while True:
        current_time = time.time()

        # Check if 6 minutes have passed since last task_2
        if current_time - last_task_2_time >= task_2_interval:
            print("Running task_2...")
            task_2(first_run=first_task_2_run)
            first_task_2_run = False
            last_task_2_time = current_time
            print("Task_2 completed, resuming task_1...")

        # Run task_1
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
