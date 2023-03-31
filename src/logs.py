import os
import time
from src.args import args

log_file = "./logs/log.txt"

def log(msg):
    # Create log directory if it doesn't exist
    if not os.path.exists("./logs/"):
        os.makedirs("./logs/")

    with open(log_file, 'a') as file:
        file.write(msg + "\n")


def debug_log(msg):
    log(msg)
    if args.debug:
        print(msg)


def log_screenshot(driver):
    # Create log directory if it doesn't exist
    if not os.path.exists("./logs/screenshots/"):
        os.makedirs("./logs/screenshots/")

    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime())
    driver.save_screenshot(f"./logs/screenshots/screenshot-{now}.png")

    return f"screenshot-{now}.png"