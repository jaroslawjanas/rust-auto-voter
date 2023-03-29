import glob
from vote import vote_on_server
import json
import pickle
from datetime import datetime
import os
import time
import args

def main():
    # Cookie search
    steam_cookies = "./config/steam_cookies"
    cookies_files = glob.glob(steam_cookies + "/*.pkl")
    print(f"Found {len(cookies_files)} cookie files")

    # Vote urls search
    vote_urls_file = "./config/urls.json"
    with open(vote_urls_file, 'r') as file:
        vote_urls = json.load(file)
    print(f"Found {len(vote_urls)} vote urls")

    # Initial vote
    print("Beginning initial vote")
    vote_loop(vote_urls, cookies_files)

    last_vote = datetime.now()
    while True:
        # Get the current time
        time_since = datetime.now() - last_vote

        # Check if it's been 5 hours since the last execution
        if time_since.seconds > 60*60*args.args.interval:
            print(f"Beginning vote at {datetime.now().strftime('%H:%M:%S')}")
            vote_loop(vote_urls, cookies_files)
        else:
            # Print the time left in hours
            print(
                f"Next voting attempt in {round((60*60*5 - time_since.seconds)/60/60, 2)} hours")

        # Wait for an hour before checking again
        time.sleep(60*60)


def vote_loop(vote_urls, cookies_files):
    # Results dict
    results = {
        "success": [],
        "fail": []
    }
    start_time = datetime.now()

    # Vote loop
    for vote_url in vote_urls:
        print(f"Beggining vote loop for {vote_url}")

        for cookies_file in cookies_files:
            cookies = pickle.load(open(cookies_file, "rb"))
            result = vote_on_server(vote_url, cookies)

            if result:
                results["success"].append((cookies_file, vote_url))
            else:
                results["fail"].append((cookies_file, vote_url))

    # Results
    print(f"Finished voting at {datetime.now().strftime('%H:%M:%S')}")
    print(f"Made {len(results['success'])} successful votes")
    print(f"Failed {len(results['fail'])} votes")

    log_to_file(results, start_time)


def log_to_file(results, start_time):
    # Log file open
    log_file = "./logs/log.txt"

    # Create lof directory if it doesn't exist
    if not os.path.exists("./logs/"):
        os.makedirs("./logs/")

    file = None
    if os.path.exists(log_file):
        file = open(log_file, 'a')
    else:
        file = open(log_file, 'w')

    # Log file results
    file.write(f"Started voting at {start_time.strftime('%d/%m/%Y %H:%M:%S')}\n")
    file.write(
        f"Finished voting at {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")

    file.write(f"Made {len(results['success'])} successful votes\n")
    for success in results["success"]:
        file.write(f"{success[0]}\t{success[1]}\n")

    file.write(f"Failed {len(results['fail'])} votes\n")
    for fail in results["fail"]:
        file.write(f"{fail[0]}\t{fail[1]}\n")

    file.write("\n")
    file.close()


if __name__ == "__main__":
    main()
