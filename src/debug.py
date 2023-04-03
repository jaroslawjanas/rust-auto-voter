import time
from src.args import args

def slow():
    if args.slow > 0:
        time.sleep(args.slow)