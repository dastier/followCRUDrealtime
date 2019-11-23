FROM python:3.8.0

RUN mkdir /app

WORKDIR /app

COPY . /app

RUN pip3 install Flask flask_script flask_migrate flask-socketio psycopg2-binary

ENTRYPOINT ["python3", "manage.py", "runserver"]