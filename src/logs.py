import os

log_file = "./logs/log.txt"

def log(msg):
    # Create log directory if it doesn't exist
    if not os.path.exists("./logs/"):
        os.makedirs("./logs/")

    with open(log_file, 'a') as file:
        file.write(msg)