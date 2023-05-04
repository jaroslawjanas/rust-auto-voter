import json
from datetime import datetime
import time
from src.action_sequence import action_sequence
from src.driver_setup import get_driver
from src.args import args


def main():
    # Url search
    vote_url_file = "./config/url.json"
    with open(vote_url_file, 'r') as file:
        vote_url = json.load(file)
    
    if len(vote_url) == 0:
        print("No urls found, exiting")
        return
    elif len(vote_url) > 1:
        print("Multiple urls found, exiting")
        return
    
    # Getting driver
    driver = get_driver()

    # Initial vote
    print("Beginning initial loop")
    action_sequence(driver, vote_url)

    last_action = datetime.now()
    while True:
        # Get the current time
        time_since = datetime.now() - last_action

        # Check if it's been 5 hours since the last execution
        if time_since.seconds > 60*60*args.interval:
            last_action = datetime.now()
            print(f"Beginning at {datetime.now().strftime('%H:%M:%S')}")
            action_sequence(driver, vote_url)
        else:
            # Print the time left in hours
            print(
                f"Next attempt in {round((60*60*args.interval - time_since.seconds)/60/60, 2)} hours")

        # Wait for an hour before checking again
        time.sleep(60*60)


if __name__ == "__main__":
    main()
