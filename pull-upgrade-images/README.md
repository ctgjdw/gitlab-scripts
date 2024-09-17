# Pulling Upgrade Images for Gitlab

`pull_upgrade_images.py` will pull the required images for `Gitlab` and `Gitlab Runners` according to the recommended upgrade path as defined in `upgrade-path.txt`

## Requirements

- [Download msedgedriver for Selenium](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)
- Add the above directory containing the `msedgedriver` binary to your PATH environment variable, so that `msedgedriver` can be called in your shell/terminal
- `pip install poetry` and `poetry install` to install the dependencies

## To Run

1. cd `pull-upgrade-images`
2. Run `poetry shell` to activate your environment
3. Run `python pull_upgrade_images.py <GITLAB_VERSION> <"ce" / "ee">`, where `ce` is community edition and `ee` is enterprise edition
    1. `-o` / `--output-file` (optional) - to output the required images to a text file for your own docker download scripts to pull
    2. `-r` / `--get-runner-image` (optional, default = False) - whether to get the gitlab ci-runner image as well. This will get only the final version's image