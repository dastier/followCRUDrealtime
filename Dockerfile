FROM python:3.8.0

RUN mkdir /app

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "manage.py", "run"]