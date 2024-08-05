FROM python:3.12

ENV DOCKERIZE_VERSION v0.6.1

RUN mkdir -p /app
WORKDIR /app
ADD . /app/

VOLUME /reports

RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz
RUN tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN pip install pipenv
RUN pipenv install --system --dev --deploy

CMD /app/compose/test/django/start.sh
