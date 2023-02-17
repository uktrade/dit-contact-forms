#!/bin/bash -xe

# ----------------- INITIALIZE -------------
# ----------------- instruction -------------
# when first building the environment and running django-compose up for the first time uncomment the following block
# of commands to get, prepare and import the content, generate keywords and create and populate the index.
#
# Alternatively uncomment `sleep infinity` and run the manage.py commands in a terminal manually, in the order they
# appear.
#
# it may take up to an hour to complete all commands, depending up machine,
#
# These commands only need running once, unless you destroy the containers and need to build the environment
# from scratch again
# ----------------- commands ----------------
# sleep infinity
python manage.py collectstatic --noinput
# -------------------------------------------

# ----------------- ONGOING DEVELOPMENT -----
# ----------------- instruction -------------
# Once the first build of the environment and import of the content is done remove the comments for of the following
# so that the django server starts when running django-compose up.
# Also do not forget to comment out the command in the INITIALISE SECTION
# ----------------- commands ----------------
python manage.py runserver 0.0.0.0:8000
# --------------------------------------------

# ----------------- instruction -------------
# run this in a terminal if you need to need to re-install dependencies
# ----------------- commands ----------------
# pip install -r requirements/development.txt
# -------------------------------------------

# ----------------- ENVIRONMENT -------------
# ----------------- instruction -------------
# To destroy and rebuild:
# The following copmmand will stop the containers but not destroy them, `docker-compose up` will allow you to
# resume development without the need to re-import the content
# alternatively `docker-compose down` will both stop AND remove containers in one command)
# ----------------- commands ----------------
# $ docker-compose -f development.yml stop
# $ docker-compose -f development.yml rm
# $ docker-compose -f development.yml build
# $ docker-compose -f development.yml up
# --------------------------------------------
