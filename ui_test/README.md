# Ui Testing

## Setup

1) Ensure you download the latest chromedriver from the URL below:

https://chromedriver.chromium.org/downloads

Then move the binary to /usr/bin which is on your PATH already or create a folder and add it to the PATH environment variable I.E export PATH=$PATH:~/webdriver

2) Install dependencies: `$ pip install -r requirements/development.txt`

It's advised to run the command above on an isolated environment, like for example using virtualenv.

## Run the tests

Execute the following command to run the tests: `pytest ui_test/specs`
