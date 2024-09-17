import sys
from argparse import ArgumentParser, BooleanOptionalAction
from logging import Logger, StreamHandler

from selenium import webdriver
from selenium.webdriver.common.by import By
import pyperclip  # To access the clipboard
import time

LOGGER = Logger(__file__)
LOGGER.addHandler(StreamHandler(sys.stdout))

def get_upgrade_path_via_selenium(current_ver: str, gitlab_edition: str):
    LOGGER.info("Retrieving upgrade path from the Official Gitlab Upgrade Tool for Gitlab %s - %s", current_ver, gitlab_edition)

    # Initialize the WebDriver for Edge
    driver = webdriver.Edge()

    try:
        # Open the URL
        driver.get(f"https://gitlab-com.gitlab.io/support/toolbox/upgrade-path/?current={current_ver}&distro=docker&edition={gitlab_edition}")

        # Wait for the page to fully load
        time.sleep(4)

        # Find the "Copy to Clipboard" button by its XPath
        copy_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/button')

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

def get_gitlab_image_tag(version: str, gitlab_edition: str) -> str:
    return f"gitlab/gitlab-{gitlab_edition}:{version}-{gitlab_edition}.0"

def main(args):
    upgrade_path = get_upgrade_path_via_selenium(args.current_version, args.gitlab_edition)
    versions = [v.strip() for v in upgrade_path.split("=>")]
    LOGGER.info("Upgrade path is: %s", versions)
    
    final_version = f"{versions[-1][0:-2]}.0"
    docker_images = [f"{get_gitlab_image_tag(i, args.gitlab_edition)}\n" for i in versions]

    if args.get_runner_image:
        docker_images.append(f"gitlab/gitlab-runner:v{final_version}")

    if (output_path:=args.output_file):
        LOGGER.info("Writing gitlab upgrade images to %s", output_path)
        with open(output_path, "w", encoding="utf-8") as file:
            file.writelines(docker_images)


if __name__ == "__main__":
    parser = ArgumentParser(description="This CLI will pull and package the required docker images for upgrading Gitlab and it's runners.")
    parser.add_argument("current_version", help="The current version to upgrade from.")
    parser.add_argument("gitlab_edition", help="The gitlab edition. (ce/ee)", default="ce")
    parser.add_argument("--get-runner-image", "-r", required=False, help="Gets the gitlab runner image as well.", default=False, action=BooleanOptionalAction)
    parser.add_argument("--output-file", "-o", required=False, help="Output the required docker images to pull into a text file, where the value is the file name")
    main(parser.parse_args())