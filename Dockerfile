FROM python:3.8.0

LABEL Author="Aliaksei Piatrouski"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app

WORKDIR /app

COPY app /app


RUN chmod u+x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]