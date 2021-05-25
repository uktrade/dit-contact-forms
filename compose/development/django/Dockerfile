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

RUN apt-get install -y wget

RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz
RUN tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN pip install pipenv
RUN pipenv install --system --dev --deploy

CMD /app/compose/development/django/start.sh
