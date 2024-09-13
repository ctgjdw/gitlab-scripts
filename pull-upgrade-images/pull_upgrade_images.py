import sys
from argparse import ArgumentParser
from logging import Logger, StreamHandler

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pyperclip  # To access the clipboard
import time

LOGGER = Logger(__file__)
LOGGER.addHandler(StreamHandler(sys.stdout))

def get_upgrade_path_via_selenium(current_ver: str, gitlab_edition: str):
    LOGGER.info("Retrieving upgrade path from the Official Gitlab Upgrade Tool for Gitlab %s - %s", current_ver, gitlab_edition)
    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    # Initialize the WebDriver with headless options
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Open the URL
        driver.get(f"https://gitlab-com.gitlab.io/support/toolbox/upgrade-path/?current={current_ver}&edition={gitlab_edition}")

        # Wait for the page to fully load
        time.sleep(4)

        # Find the "Copy to Clipboard" button by its CSS selector or XPath
        copy_button = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[3]/button')

        # Click the "Copy to Clipboard" button
        copy_button.click()

        # Wait briefly to ensure clipboard is updated
        time.sleep(1)

        # Retrieve the copied text from the clipboard
        return pyperclip.paste()
    except Exception as e:
        Logger.error("An error occurred when trying to retrieve the upgrade path from the website: %s", e, exc_info=e)
    finally:
        # Close the browser
        driver.quit()

def main(args):
    upgrade_path = get_upgrade_path_via_selenium(args.current_version, args.gitlab_edition)
    versions = [v.strip() for v in upgrade_path.split("=>")]
    final_version = versions[-1]
    docker_images = [i for i in versions]

    if (output_path:=args.output_file):
        with open(output_path, "w", encoding="utf-8") as file:
            file.writelines()


if __name__ == "__main__":
    parser = ArgumentParser(description="This CLI will pull and package the required docker images for upgrading Gitlab and it's runners.")
    parser.add_argument("current_version", help="The current version to upgrade from.")
    parser.add_argument("gitlab_edition", help="The gitlab edition. (ce/ee)", default="ce")
    parser.add_argument("--output-file", "-o", required=False, help="Output the required docker images to pull into a text file, where the value is the file name")
    main(parser.parse_args())