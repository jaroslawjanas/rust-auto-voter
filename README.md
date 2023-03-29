# Rust Auto Voter
**Rust Auto Voter** is a Python program that automates voting on **rust-servers.net**, a website where Rust game servers are listed and ranked based on the number of votes they receive. The program uses the **Selenium WebDriver** library to simulate human interaction with the website, and can be configured to vote for multiple Rust servers at set intervals.

The program requires the user to have a valid Steam account and to generate Steam login cookies, which are used to bypass the website's login process. Additionally, the user must provide the program with the URLs of the Rust servers they wish to vote for, which can be added to the `urls.json` configuration file.

The program is designed to be run on Linux or Windows and requires the user to download the appropriate Chromium browser and driver for their system from the Chromium Browser Snapshots website.

## Environment Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/rust-auto-voter.git
cd rust-auto-voter
```

2. Create a new conda environment using the environment.yaml file:
```bash
conda env create -f environment.yaml
conda activate rust-auto-voter
```

3. Download Chromium binary and driver for your system from [here](https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html).

- Find the latest version in a file called `LAST_CHANGE`.
- Download the binary and the driver. Most people will either want to download from Linux_x64 or Win_x64 directories.
- The files you want to download will be packaged into a zip archive with the following naming scheme `chrome-*.zip` and `chromedriver_*.zip`. For example, for Linux it will be `Linux_x64/<version>/chrome-linux.zip` and `Linux_x64/<version>/chromedriver_linux64.zip`.
Extract the downloaded files and move them to the `./browser` directory in the project folder.

## Configuration Setup

1. Add your server URL(s) in `./config/urls.json` in JSON format, like so:
```json
["<url1>", "<url2>"]
```

2. Run `python cookie_getter.py` and log in to your Steam account. Once you are logged in, press Enter and specify the account's name. You can add as many accounts as you want.


## Running the Program

To run the program, use the following command:

```bash
python main.py [--debug] [--browser_path <path>] [--driver_path <path>] [--interval <hours>]
```

## Arguments

**--debug** (optional) - Enters debugging mode (default: false)

**--browser_path <path>** (optional) - Manually specify Chromium browser path (*default: dynamic*)

**--driver_path <path>** (optional) - Manually specify Chromium driver path (*default: dynamic*)

**--interval <hours>** (optional) - How many hours between each voting loop (*default: 5*)

For example, to run the program in debugging mode with a specific browser and driver path, use:

```bash
python main.py --debug --browser_path "/path/to/chrome.exe" --driver_path "/path/to/chromedriver"
```