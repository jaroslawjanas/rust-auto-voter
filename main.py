import glob
from src.vote import vote_on_server
import json
import pickle
from datetime import datetime
from src.logs import log
from src.logs import debug_log
import time
from src.args import args


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

    if len(vote_urls) == 0:
        print("No vote urls found, exiting")
        return

    if len(cookies_files) == 0:
        print("No cookies found, exiting")
        return

    # Initial vote
    print("Beginning initial vote")
    vote_loop(vote_urls, cookies_files)

    last_vote = datetime.now()
    while True:
        # Get the current time
        time_since = datetime.now() - last_vote

        # Check if it's been 5 hours since the last execution
        if time_since.seconds > 60*60*args.interval:
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

    debug_log(f"Started voting at {datetime.now().strftime('%H:%M:%S')}")

    # Vote loop
    for vote_url in vote_urls:
        if vote_url == "":
            debug_log(f"Empty vote url found, skipping")
            continue

        debug_log(f"Beggining vote loop for {vote_url}")

        for cookies_file in cookies_files:
            debug_log(f"Beggining voting using {cookies_file}")
            cookies = pickle.load(open(cookies_file, "rb"))
            result = vote_on_server(vote_url, cookies)

            if result:
                results["success"].append((cookies_file, vote_url))
            else:
                results["fail"].append((cookies_file, vote_url))

    # Results
    log(f"Finished voting at {datetime.now().strftime('%H:%M:%S')}")
    print(f"Made {len(results['success'])} successful votes")
    print(f"Failed {len(results['fail'])} votes")

    # Log results
    log(f"Made {len(results['success'])} successful votes")
    for success in results["success"]:
        log(f"{success[0]}\t{success[1]}")

    log(f"Failed {len(results['fail'])} votes")
    for fail in results["fail"]:
        log(f"{fail[0]}\t{fail[1]}")

    log("-"*50)


if __name__ == "__main__":
    main()
