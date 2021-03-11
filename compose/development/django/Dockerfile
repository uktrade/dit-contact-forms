#
# This is used for development only, we are not worried about image size
# Instead we prefer build speed and readability this is why RUN commands are not merged
#
FROM python:3.6

ENV DOCKERIZE_VERSION v0.6.1

RUN mkdir -p /app
WORKDIR /app
ADD . /app/


VOLUME /reports

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash
RUN apt-get install -y wget virtualenv nodejs


RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz
RUN tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN pip install pipenv
RUN pipenv install --system --dev --deploy
RUN npm set unsafe-perm true

RUN npm install --global gulp-cli


# install and build gov.uk frontend.
RUN npm install
# see: https://github.com/sass/node-sass/issues/1579
RUN npm rebuild node-sass
RUN gulp build

CMD /app/compose/development/django/start.sh
