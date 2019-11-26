FROM python:3.8.0

LABEL Author="Aliaksei Piatrouski"

RUN mkdir /app

WORKDIR /app

COPY . /app

RUN chmod u+x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]