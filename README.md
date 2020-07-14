# dit-contact-forms

This service is used by people who have queries about exporting goods from the UK.

# TL;DR

To setup this project for local development with docker

1. run `make template-files`
2. update both `.env` and `.env.test` (vault can be found at https://vault.ci.uktrade.digital/ui/vault/secrets/dit%2Ftrade-helpdesk/list/helpdesk/)
3. run `make build`
4. run `make setup`

> `make help` is your friend

## Requirements

- Python 3
- Node [Active LTS][1] version (Current Active version is v10)
- Docker (if developing locally with docker)

#### Optional. Only required for testing contact form submissions to zenddesk

- Directory Forms API (https://github.com/uktrade/directory-forms-api)
  - redis (installed locally)
  - postgres (installed locally)

### Install using Docker

If you have Docker installed, you can run this service without needing to set up the database yourself, worrying about
virtual environments - it's all within the Docker instance.

- Docker for mac - https://hub.docker.com/editions/community/docker-ce-desktop-mac
- Docker for Win - https://download.docker.com/win/static/stable/x86_64/

## Installation

### Directory Forms API (Optional only required when testing contact form submissions to zenddesk)

clone the directory

```
git clone https://github.com/uktrade/directory-forms-api.git .
```

create a hosts file entry for

`127.0.0.0.1 forms.trade.great`

Follow installation and setup instructions in https://github.com/uktrade/directory-forms-api/blob/develop/README.md

NB: add the following entries to the env file

```
HEALTH_CHECK_TOKEN=""
DEFAULT_FROM_EMAIL=""
REDIS_CELERY_URL="redis://localhost:6379"
GOV_NOTIFY_LETTER_API_KEY=debug
DJANGO_SECRET_KEY=debug
FEATURE_ENFORCE_STAFF_SSO_ENABLED=False
STAFF_SSO_AUTHBROKER_URL=
AUTHBROKER_CLIENT_ID=
AUTHBROKER_CLIENT_SECRET=
```

after running `make debug` in a terminal

create a superuser by running the following in a terminal

```
export DATABASE_URL=postgres://debug:debug@localhost:5432/directory_forms_api_debug
./manage.py createsuperuser
```

then run `make debug_webserver` to start the server

access the application admin screens locally in you browser with the url http://forms.trade.great:8011/admin

Click the add button in the Client section and add `helpdesk` as the name of the client then click submit. This will
generate the user identifier and accss key that you need to add to the .env file for the `dit_helpdesk` application

### DIT Contact Forms

First clone the repo

```bash
git@github.com:uktrade/dit-contact-forms.git .

```

then using a terminal move inside of the folder:

```bash
cd dit-contact-forms
```

#### Frontend static asset installation

First we need to install [GOV.UK Frontend][2] and
[GOV.UK country and territory autocomplete][3] (Which will also also install the required [Accessible Autocomplete][4]
dependency), and other front end dependencies.

This is all done by going to the project root folder, which contains `package.json`. Then run:

```bash
npm install
```

This will install all of the packages needed to build the front end static assets.

To build and move all of the static assets:

```bash
npm run build
```

`npm run` will show a list of all of the commands available, including linting.

#### set environment variables

copy the two development environment variables files

```
make template-files
```

add entries where necessary (see comments for guidance)

You will need to access [Helpdesk Vault][5] to get the required environment variable secrets to use them in the file.
To do so you will need to generate a github personal access token. This is needed to log into vault.
Go here: [Vault][6] click `Generate new token` and make sure it has these scopes: `read:org`, `read:user`.
Once you've done that, head over to [Vault][7] and login with the token. You'll need to select github
as your login option.

#### Install for development with Docker

Make sure that Docker is installed and running.

##### Initial setup run

This intial set up will take several minutes (depending upon machine and internet speed) to set up and fully import
all content, on subsequent runs it will on take a minute or so to be up and running for development.

The initial run (this section) only needs to be done when building a new or fresh docker container. Once this section
has been done and as long as the docker images are not destroyed.

To build the docker containers, run:

```bash
make build
```

To run the Docker containers, run:

```bash
make up
```

Open a second terminal and run the following command to activate a shell into the docker instance
for the trade helpdesk app with the command.

```
docker-compose exec contact_forms /bin/bash
```

refer to "Running, then shelling in" section below

### Running tests with Docker development deployment

refer to the section `Running, then shelling in` above to get a shell in the running docker instance

From within the docker shell terminal run the following command for full tests:

```
coverage run manage.py test contact_forms --settings=config.settings.test
```

for testing a single app run i.e. the admin app:

```
coverage run manage.py test admin.tests --settings=config.settings.test
```

for testing a single app's test module run i.e. the test_views in the the hierarchy app:

```
coverage run manage.py test admin.tests.test_views --settings=config.settings.test
```

and so on.

for coverage reports run

```
coverage -d reports html
```

you will then be able to access the coverage report html from within your project folder's root
from your host machine at /reports

### Running tests and generating coverage with Docker

```bash
make test

```

This will display in the shell the following:

- all tests, showing passes and failures
- coverage report

it will also generate the following reports into folder `reports` :

- xunit coverage report file
- xml coverage report file
- html coverage report

## Creating Docker container for CircleCI

```bash
export VERSION=1.0.0 # Increment this version each time when you edit Dockerfile.
docker login # Ask webops for Docker Hub access to the ukti group.
docker build -f Dockerfile -t dit-contact-forms .
docker tag dit-contact-forms:latest ukti/dit-contact-forms:${VERSION}
docker tag dit-contact-forms:latest ukti/dit-contact-forms:latest
docker push ukti/dit-contact-forms:${VERSION}
docker push ukti/dit-contact-forms:latest
```

[1]: https://nodejs.org/en/about/releases/
[2]: https://github.com/alphagov/govuk-frontend
[3]: https://github.com/alphagov/govuk-country-and-territory-autocomplete
[4]: https://github.com/alphagov/accessible-autocomplete
[5]: https://vault.ci.uktrade.io/ui/vault/secrets/dit%2Ftrade-helpdesk/list/helpdesk/
[6]: https://github.com/settings/tokens
[7]: https://vault.ci.uktrade.io
