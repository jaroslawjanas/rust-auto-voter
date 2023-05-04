import argparse

# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--debug", help="Enters debugging mode (default: false)", action="store_true", default=False)
parser.add_argument("--slow", help="Sleep for a specified amount of seconds after each operation, used for testing (default: 0)", type=int, default=0)
parser.add_argument("--headless", help="Enters debugging mode (default: false)", action="store_true", default=False)
parser.add_argument("--browser_path", help="Manualy specify Chromium browser path (default: dynamic)", type=str)
parser.add_argument("--driver_path", help="Manualy specify Chromium driver path (default: dynamic)", type=str)
parser.add_argument("--interval", help="How many hours between each voting loop (deafult: 5)", type=int, default=5)
parser.add_argument("--width", help="Browser window width (default: 960)", type=int, default=960)
parser.add_argument("--height", help="Browser window height (default: 960)", type=int, default=960)
parser.add_argument("--incognito", help="Runs the browser in incognito mode (default: false)", action="store_true", default=False)

args = parser.parse_args()