# Ui Testing

## Setup

1) Ensure you download the latest chromedriver from the URL below:

https://chromedriver.chromium.org/downloads

Note that you should try to match the chromedriver with your chrome version I.E if you have chrome version 79, ensure to download the chromedriver version binary 79 as well.

Then move the binary to /usr/bin which is on your PATH already or create a folder and add it to the PATH environment variable I.E export PATH=$PATH:~/webdriver

2) Install dependencies: `$ pip install -r requirements/development.txt`

It's advised to run the command above on an isolated environment, like for example using virtualenv.

## Run the tests

Execute the following command to run the tests: `pytest ui_test/specs`

## Creating Docker container for CircleCI

```bash
export VERSION=1.0.0 # Increment this version each time when you edit Dockerfile.

docker login # Ask webops for Docker Hub access to the ukti group.
docker build -f ui_test/Dockerfile -t dit-contact-forms-test .

docker tag dit-contact-forms-test:latest ukti/dit-contact-forms-test:${VERSION}
docker tag dit-contact-forms-test:latest ukti/dit-contact-forms-test:latest

docker push ukti/dit-contact-forms-test:${VERSION}
docker push ukti/dit-contact-forms-test:latest
```

You image should be now listed at [Docker Hub](https://cloud.docker.com/u/ukti/repository/docker/ukti/dit-contact-forms-test/tags).
