# Pulling Upgrade Images for Gitlab

`pull_upgrade_images.py` will pull the required images for `Gitlab` and `Gitlab Runners` according to the recommended upgrade path as defined in `upgrade-path.txt`

## Requirements

- [Download ChromeDriver for Selenium](https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json)
- Add the above `ChromeDriver` binary to your System Path, so that `chromedriver` can be called in your shell/terminal
- `pip install poetry` and `poetry install` to install the dependencies

## To Run

1. cd `pull-upgrade-images`
2. Run `poetry shell` to activate your environment
3. Run `python pull_upgrade_images.py <GITLAB_VERSION> <"ce" / "ee">`, where `ce` is community edition and `ee` is enterprise edition
    1. `-o` / `--output-file` (optional) - to output the required images to a text file for your own docker download scripts to pull